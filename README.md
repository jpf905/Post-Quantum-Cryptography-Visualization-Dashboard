# **Post-Quantum Cryptography (PQC) Visualization Dashboard**

A data-driven Streamlit dashboard to explore performance, key sizes, and security levels of post-quantum cryptosystems (KEMs and Signatures). Includes simple ML models to predict performance from features.
<img width="1628" height="971" alt="Screen Shot 2025-10-14 at 8 21 47 PM" src="https://github.com/user-attachments/assets/3d1b6346-0c2f-49d6-8e85-f2b8a33c9c22" />

## **Notes**
- The ML tab trains a separate regression for each timing metric using a Pipeline(OneHotEncoder + StandardScaler + RandomForest).
- The app caches models to keep the UI snappy; tweak `N_ESTIMATORS` in `src/train_models.py` to trade speed vs. accuracy.


## **Bring your own data**
Replace `data/benchmarks.csv` with a CSV that has these columns (extra columns are fine):

- `scheme`: `KEM` or `SIG`
- `family`: e.g., CRYSTALS-Kyber, SPHINCS+, Classic McEliece, CRYSTALS-Dilithium
- `category`: `lattice`, `hash`, `code`, etc.
- `variant`: e.g., Kyber768, Dilithium3
- `security_level`: NIST level (1,2,3,4,5)
- `impl`: implementation tag: `ref`, `avx2`, etc.
- Sizes (bytes): `pk_bytes`, `sk_bytes`, `ct_or_sig_bytes`
- Timings (ms): `keygen_ms`, `encap_ms`, `decap_ms`, `sign_ms`, `verify_ms` (leave irrelevant cells blank)

