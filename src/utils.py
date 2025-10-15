from typing import List
def nice_bytes(x: float) -> str:
    # human-readable bytes
    if x is None:
        return "—"
    units = ["B","KB","MB","GB"]
    k = 0
    while x >= 1024 and k < len(units)-1:
        x /= 1024.0
        k += 1
    return f"{x:.1f} {units[k]}"

TARGETS: List[str] = ["keygen_ms","encap_ms","decap_ms","sign_ms","verify_ms"]
CAT_FEATS: List[str] = ["scheme","family","category","variant","impl"]
NUM_FEATS: List[str] = ["security_level","pk_bytes","sk_bytes","ct_or_sig_bytes"]
