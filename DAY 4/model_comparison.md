# Four-Model Comparison

Model cards and Ollama library pages were checked on **2026-10-02**. Catalog sizes can change. Download figures below are the size shown by the current Ollama library for the selected/default tag; they are approximate and are not asserted to be exact Q4_K_M files. The gpt-oss Ollama build specifically uses MXFP4.

| Worksheet item | Qwen | Mistral | IBM Granite | OpenAI gpt-oss |
|---|---|---|---|---|
| Full model/version | Qwen3-8B | Mistral-7B-Instruct-v0.3 | Granite-3.3-8B-Instruct | gpt-oss-20b |
| Publisher | Alibaba Qwen | Mistral AI | IBM Granite | OpenAI |
| Sizes available in family | Ollama lists 0.6B, 1.7B, 4B, 8B, 14B, 30B-A3B, 32B and 235B-A22B variants | Selected library build is 7B; v0.3 is the function-calling revision | Ollama lists 2B and 8B | 20B and 120B variants |
| Selected size / Ollama download | 8.2B; `qwen3:8b`, about 5.2 GB | 7B; `mistral:7b`, about 4.4 GB | 8B; `granite3.3:8b`, about 4.9 GB | 21B total; `gpt-oss:20b`, about 14 GB |
| Total / active parameters | 8.2B / 8.2B, dense | 7B / 7B, dense | 8B / 8B, dense | 21B / 3.6B active (MoE) |
| Context window | 32,768 native; up to 131,072 with YaRN per card. Ollama library lists 40K for this tag. | Ollama library lists 32K | 128K | 128K on Ollama; model card documents long-context use |
| Exact license | Apache-2.0 | Apache-2.0 | Apache-2.0 | Apache-2.0 |
| Commercial use allowed? | Yes, under Apache-2.0 terms | Yes, under Apache-2.0 terms | Yes, under Apache-2.0 terms | Yes, under Apache-2.0 terms |
| Extra conditions | Preserve license/copyright notices and identify material changes as Apache-2.0 requires. Check the exact artifact/revision before redistribution. | Same Apache-2.0 notice and change-marking obligations. | Same Apache-2.0 notice and change-marking obligations. | Same Apache-2.0 obligations; separately follow model-card safety guidance and applicable law. |
| Tool/function calling stated? | Yes; card describes tool calling and agent use. | Yes; v0.3 card includes function-calling examples. | Yes; card lists function-calling tasks. | Yes; card explicitly describes function calling and agentic tool use. |
| GGUF/Ollama build available? | Yes, Ollama `qwen3` family | Yes, Ollama `mistral` family | Yes, Ollama `granite3.3` family | Yes, Ollama `gpt-oss` family |
| Memory estimate at 8K | 6.58 GB, using 8.2B and generic Q4_K_M formula | 5.62 GB, using 7B and Q4_K_M | 6.42 GB, using 8B and Q4_K_M | 16.86 GB using generic Q4_K_M approximation; not the actual MXFP4 runtime size |
| Predicted to fit this machine? | Yes on installed-RAM arithmetic; not run-verified | Yes on installed-RAM arithmetic; not run-verified | Yes on installed-RAM arithmetic; not run-verified | No by the generic Q4 estimate; Ollama reports a 14 GB download and this machine has 15.69 GB total RAM, so a usable runtime budget is not established |

## Licence Questions

All four selected official instruct/reasoning cards identify Apache-2.0, so no licence difference appears among these four selected models. That does not certify every model, base model, derivative, fine-tune, or future revision in each publisher's wider family; check the exact repository's LICENSE before use. Apache-2.0 allows commercial use and redistribution subject to its conditions. Section 4(b) says: "You must cause any modified files to carry prominent notices stating that You changed the files." Section 4 also requires a copy of the license and retention of applicable copyright, patent, trademark, and attribution notices. Based on the selected cards, all four can be used commercially without first requesting a separate licence, while still complying with those terms.

The cards explicitly identify tool/function calling for all four choices. Mistral v0.3 demonstrates function-calling interfaces; Qwen3 describes agentic tool use; Granite lists function-calling tasks; gpt-oss details function calling and agentic use. Mistral's card is particularly direct about a limitation: it says the model does not include moderation mechanisms. Granite also points readers to inherited limitations from its base model. These disclosures matter for deployment; a permissive licence does not supply safety controls.

## Sources

- [Qwen/Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B) and [Ollama qwen3 library](https://ollama.com/library/qwen3)
- [Mistral-7B-Instruct-v0.3 model card](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) and [Ollama mistral library](https://ollama.com/library/mistral)
- [Granite-3.3-8B-Instruct model card](https://huggingface.co/ibm-granite/granite-3.3-8b-instruct) and [Ollama granite3.3 library](https://ollama.com/library/granite3.3)
- [openai/gpt-oss-20b model card](https://huggingface.co/openai/gpt-oss-20b) and [Ollama gpt-oss library](https://ollama.com/library/gpt-oss)
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)