# **Post-Quantum Cryptography (PQC) Visualization Dashboard**

A data-driven Streamlit dashboard to explore performance, key sizes, and security levels of post-quantum cryptosystems (KEMs and Signatures). Includes simple ML models to predict performance from features.
<img width="1628" height="971" alt="Screen Shot 2025-10-14 at 8 21 47 PM" src="https://github.com/user-attachments/assets/3d1b6346-0c2f-49d6-8e85-f2b8a33c9c22" />

## **Project Summary**
This project delivers an interactive data-driven visualization of post-quantum cryptographic systems, combining advanced analytics with accessible design. Built in Streamlit, the dashboard allows users to explore the performance, key sizes, and security levels of next-generation encryption algorithms such as ML-KEM, ML-DSA, Falcon, SPHINCS+, McEliece, BIKE, and NTRU. Using a clean, structured dataset and machine learning regression models, the tool reveals how different cryptosystems balance efficiency and robustness across implementations and security levels. Ultimately, this project bridges data science and cybersecurity, providing a clear, visual framework for understanding the trade-offs shaping the future of quantum-resistant encryption.<br>

[![Watch the video!]](https://youtu.be/jL0yL0gfF5I)

https://youtu.be/jL0yL0gfF5I

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

<img width="1498" height="909" alt="Screen Shot 2025-10-14 at 8 22 35 PM" src="https://github.com/user-attachments/assets/819b7d2b-7577-4b3b-b3fb-662462fb83ce" />
<img width="656" height="655" alt="Screen Shot 2025-10-14 at 8 23 19 PM" src="https://github.com/user-attachments/assets/fea5f668-aecc-481f-8fb0-510db2911937" />
<img width="1331" height="899" alt="Screen Shot 2025-10-14 at 8 24 00 PM" src="https://github.com/user-attachments/assets/96ab8004-662e-471a-b679-82177fe18f05" />
