# Day 4 Estimate Sheet

**Recorded:** 2026-10-02
**Machine:** 15.69 GB installed system RAM; Intel Iris Xe integrated graphics; no discrete GPU identified. Ollama is not installed or available on PATH.

## Formula and Hand Estimates

For parameter count $P$ in billions, precision rate $B$ bytes per parameter, and context $C$ in thousands of tokens:

- Weights = $P \times B$ GB
- KV cache = $P \times C \times 0.02$ GB
- Total = $(\text{weights} + \text{KV cache}) \times 1.10$ GB

At an 8K context:

| Model | Precision | Weights (GB) | KV (GB) | Total (GB) |
|---|---:|---:|---:|---:|
| 1.5B small | Q4_K_M | 0.85 | 0.24 | 1.20 |
| 8B mid | Q4_K_M | 4.56 | 1.28 | 6.42 |
| 8B mid | FP16 | 16.00 | 1.28 | 19.01 |
| 30B large | Q4_K_M | 17.10 | 4.80 | 24.09 |
| 70B server | Q4_K_M | 39.90 | 11.20 | 56.21 |

The hand values above match the estimator output to two decimal places:

| Model | Hand total (GB) | Program total (GB) | Difference (GB) |
|---|---:|---:|---:|
| 1.5B Q4_K_M | 1.20 | 1.20 | 0.00 |
| 8B Q4_K_M | 6.42 | 6.42 | 0.00 |
| 8B FP16 | 19.01 | 19.01 | 0.00 |
| 30B Q4_K_M | 24.09 | 24.09 | 0.00 |
| 70B Q4_K_M | 56.21 | 56.21 | 0.00 |

On this machine the first four estimates fit within 15.69 GB on paper; the 70B estimate does not. This compares a model estimate against *installed* RAM, not memory free for a model after Windows and other applications. There is no dedicated GPU, so these are CPU/system-RAM estimates, not a claim of GPU inference.

Q4_K_M reduces the 8B weight estimate from 16.00 GB to 4.56 GB, a saving of **11.44 GB in weights**. Including the same cache and overhead, the total estimate drops from 19.01 GB to 6.42 GB, a difference of **12.59 GB**.

With a 6 GB graphics card and an 8K context, 7B Q4_K_M is the largest entry among the model sizes considered that fits: its estimated total is 5.62 GB. An 8B Q4_K_M estimate is 6.42 GB, so it exceeds 6 GB.

## Estimator Results: Context and Quantization

The estimator is [vram_estimate.py](vram_estimate.py). It uses the manual's rates and 10% overhead; the figures are estimates, not measurements.

| 8B Q4_K_M context | Weights (GB) | KV (GB) | Total (GB) | Fits 8 GB by formula? |
|---:|---:|---:|---:|---|
| 4K | 4.56 | 0.64 | 5.72 | Yes, tight |
| 8K | 4.56 | 1.28 | 6.42 | Yes, tight |
| 32K | 4.56 | 5.12 | 10.65 | No |
| 128K | 4.56 | 20.48 | 27.54 | No |

Weights stay fixed while the estimated KV cache grows with context. For an agent, prior messages and tool results consume context, so long tool outputs and many conversation turns raise memory requirements even though model weights do not change. Truncation, retrieval, or shorter context limits can control this growth.

| 8B precision at 8K | Weights (GB) | Total (GB) | Fits 8 GB by formula? |
|---|---:|---:|---|
| Q3_K_M | 3.44 | 5.19 | Yes, comfortable by the manual threshold |
| Q4_K_M | 4.56 | 6.42 | Yes, but tight |
| Q5_K_M | 5.44 | 7.39 | Yes, but tight |
| Q8_0 | 8.00 | 10.21 | No |
| FP16 | 16.00 | 19.01 | No |

For an 8 GB machine I would start with Q4_K_M as a quality/size compromise, but use Q3_K_M or a smaller model if the operating system leaves insufficient free memory. Quantization reduces memory, with lower precision generally increasing quality loss; Q3 has more noticeable loss than Q4.

## Model Estimates on This Machine

These use the simplified Q4_K_M formula at 8K, including all model parameters. The gpt-oss estimate is a comparison approximation only: its Ollama release uses MXFP4 rather than Q4_K_M.

| Candidate | Parameters used | Estimated total at 8K | Formula vs 15.69 GB installed RAM |
|---|---:|---:|---|
| Qwen3-8B | 8.2B | 6.58 GB | Fits on paper |
| Mistral-7B-Instruct-v0.3 | 7B | 5.62 GB | Fits on paper |
| Granite-3.3-8B-Instruct | 8B | 6.42 GB | Fits on paper |
| gpt-oss-20b | 21B total | 16.86 GB | Exceeds installed RAM by this approximation |

For an 8B Q4_K_M model, the formula's memory-only upper bound on this machine is about 58K context tokens. That is not a validated setting and ignores operating-system memory pressure; for Qwen3-8B, the model card states 32,768 tokens natively, with longer context requiring YaRN. Ollama is unavailable here, so this does not establish that the model actually runs at 32K on this computer.

## Estimate vs Local Runtime

| Model on this machine | `ollama list` size | `ollama ps` size | Estimate | Observation |
|---|---:|---:|---:|---|
| Not available | N/A | N/A | See candidate estimates above | `ollama` is not installed/on PATH; no local model was downloaded or loaded, so real disk and runtime values could not be recorded. |

This is an environment limitation, not a measured zero. To finish the reality check later, install Ollama, record `ollama list`, load one small model with `ollama run qwen3:1.7b`, then capture `ollama ps` while it is loaded. The actual comparison should use the loaded model's context setting and available system memory.