"""Day 4: estimate model memory needs and compare them with available RAM."""

BYTES_PER_PARAM = {
    "FP16": 2.00,
    "Q8_0": 1.00,
    "Q6_K": 0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}

KV_GB_PER_B_PER_1K = 0.02
OVERHEAD = 1.10


def estimate(params_b, precision="Q4_K_M", context_k=8):
    """Return estimated weights, KV cache, and total memory in decimal GB."""
    if params_b <= 0:
        raise ValueError("params_b must be greater than zero")
    if context_k <= 0:
        raise ValueError("context_k must be greater than zero")
    if precision not in BYTES_PER_PARAM:
        raise ValueError(f"Unknown precision {precision}. Choose from {list(BYTES_PER_PARAM)}")

    weights_gb = params_b * BYTES_PER_PARAM[precision]
    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K
    total_gb = (weights_gb + kv_gb) * OVERHEAD
    return weights_gb, kv_gb, total_gb


def verdict(total_gb, available_gb):
    if total_gb <= available_gb * 0.7:
        return "fits comfortably"
    if total_gb <= available_gb:
        return "fits, but tight"
    return "does NOT fit"


def report(name, params_b, precision, context_k, available_gb):
    weights, kv, total = estimate(params_b, precision, context_k)
    print(
        f"{name:<22} {precision:<7} {params_b:>5.1f}B  ctx {context_k:>3}K  "
        f"weights {weights:>6.2f} GB  kv {kv:>5.2f} GB  total {total:>6.2f} GB  "
        f"-> {verdict(total, available_gb)}"
    )


if __name__ == "__main__":
    AVAILABLE_GB = 15.69
    print(f"Installed system RAM used for estimate: {AVAILABLE_GB} GB\n")

    report("Qwen small", 1.5, "Q4_K_M", 8, AVAILABLE_GB)
    report("Granite / Qwen mid", 8.0, "Q4_K_M", 8, AVAILABLE_GB)
    report("Mid at FP16", 8.0, "FP16", 8, AVAILABLE_GB)
    report("Large local", 30.0, "Q4_K_M", 8, AVAILABLE_GB)
    report("Server class", 70.0, "Q4_K_M", 8, AVAILABLE_GB)

    print("\nSame 8B model, different context lengths:")
    for context_k in (4, 8, 32, 128):
        report("8B agent", 8.0, "Q4_K_M", context_k, AVAILABLE_GB)

    print("\nSame 8B model, different quantizations:")
    for precision in ("Q3_K_M", "Q4_K_M", "Q5_K_M", "Q8_0", "FP16"):
        report("8B agent", 8.0, precision, 8, AVAILABLE_GB)

    print("\nModels considered for this machine:")
    report("Qwen3-8B", 8.2, "Q4_K_M", 8, AVAILABLE_GB)
    report("Mistral-7B", 7.0, "Q4_K_M", 8, AVAILABLE_GB)
    report("Granite-3.3-8B", 8.0, "Q4_K_M", 8, AVAILABLE_GB)
    report("gpt-oss-20B", 21.0, "Q4_K_M", 8, AVAILABLE_GB)