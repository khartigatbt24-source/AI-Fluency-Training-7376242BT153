# Day 4 Recommendations and Discussion

## Recommendations

**8 GB laptop, no GPU, Unit 1 agent labs:** Use Qwen3-4B at Q4_K_M as the starting point. The Ollama library lists a roughly 2.5 GB build, and the manual's estimate formula gives about 3.21 GB for 4B/Q4_K_M/8K; Qwen3 is Apache-2.0 and its card documents tool calling. This leaves more system memory for the OS than an 8B model, though actual performance and RAM use should still be tested locally.

**Department server, one 24 GB GPU, 20 students:** Use Granite-3.3-8B-Instruct at Q4_K_M with a 4K context limit per active session and benchmark the serving engine before deployment. The base model estimate is 4.56 GB of weights; applying the manual's KV approximation to 20 simultaneous 4K sessions gives $(4.56 + 20 \times 0.64) \times 1.10 \approx 19.10$ GB, leaving limited headroom on a 24 GB GPU. A 20-session 8K configuration estimates to roughly 33.18 GB by this shared-weights/per-session-cache approximation, so it should not be assumed to fit.

**Public GitHub capstone:** Use Granite-3.3-8B-Instruct at Q4_K_M and publish the exact model revision, quantization provenance, Apache-2.0 license/notice, and any modifications. Its official card states Apache-2.0, identifies function-calling tasks, and the Ollama build is about 4.9 GB. Check the exact redistributed artifact's files and notices rather than relying on the family name alone.

## Discussion Answers

**Why can a fixed model stop fitting?** The weights are fixed, but the KV cache grows with context, and the context includes prompt history, generated tokens, and tool results. Runtime buffers and other processes also consume memory. A model that fits for a short prompt can therefore fail or slow down when the context grows.

**14B Q4 or 8B Q8 on the same hardware?** I would first compare the tasks, quality on a representative evaluation set, and actual memory at the intended context and batch size. Using the handout's approximate rates at 8K, 14B Q4 totals about 11.24 GB, while 8B Q8 totals about 10.21 GB. The 8B Q8 is slightly smaller in this estimate; the 14B Q4 may offer more capacity but could have different quality, latency, and architecture-specific cache use. I would benchmark both rather than decide from parameter count alone.

**Why might estimate and `ollama ps` disagree?** The Ollama context may be shorter than the assumed context; actual quantization and metadata/block overhead may differ from the table; and runtime, KV-cache architecture, GPU offload, allocator reservation, batch size, or other applications may change measured memory.

**Is a model with non-commercial terms useless?** No. It might still be suitable for personal learning or a non-commercial experiment if its licence permits that use, but not for a commercial product if commercial use is prohibited. For a public capstone, redistribution and demonstration terms must be checked; a GitHub repository being public does not make a restricted model license permissive.

**What is lost by using a free cloud key on a weak laptop?** The model's prompts and potentially sensitive tool data are sent to an external provider, and operation depends on internet availability, service limits, and provider terms. The user also gives up full local control over model versions, privacy, and predictable latency/cost.

## Viva Notes

- Memory formula: weights $= P \times$ bytes-per-parameter; KV $= P \times$ context-in-K $\times 0.02$ GB; total $=(\text{weights}+\text{KV})\times1.10$.
- Q4_K_M is approximated as 0.57 bytes per parameter; FP16 is 2 bytes per parameter.
- KV grows with tokens retained for attention; the parameters do not grow, but the model must retain more per-token state.
- In Q4_K_M, `Q4` indicates four-bit quantization, `K` identifies the K-quant scheme, and `M` denotes the medium variant, which uses a mixed allocation across tensor types; metadata and block structure make the effective rate about 0.57 bytes per parameter rather than exactly 0.5.
- Apache-2.0 and MIT are permissive licences that allow commercial use subject to their respective notice and other terms. Always inspect the exact model's license file.
- For a 30B MoE with 3B active per token, Q4_K_M weight storage is still based on all 30B parameters, approximately 17.10 GB; the handout's 8K cache estimate gives a 24.09 GB total. Sparse activation mainly reduces computation, not the need to store expert weights. Real KV cost depends on architecture, so the handout's formula remains an approximation.
- On an 8 GB system with long documents, use a smaller Apache-2.0 tool-capable model or lower quantization, and manage context by retrieval/chunking. Increasing context raises cache memory; long-context support does not mean long context is free.

## Result

Thus, the hand calculations and Python estimator reproduce the lab's memory estimates, and current publisher/Ollama pages establish a sourced comparison of four open-weight model families. The local-runtime comparison remains unverified because Ollama is absent on this machine; the estimates show that context length and concurrent KV caches can determine whether a model fits even when its weight file appears small enough.