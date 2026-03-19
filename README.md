# ⚡ Customer Data Vault (Bitcask-Style Storage Engine)

A high-performance, custom-built NoSQL database engine written entirely in pure Python (zero external libraries). Designed to handle high-throughput data ingestion and O(1) retrieval by implementing an append-only log architecture paired with an in-memory byte-offset index.

##The Architecture

Standard academic database models rely on sequential disk scanning, resulting in O(N) lookup times. This project implements an enterprise-grade **Bitcask-style storage model**:
1. **Append-Only I/O:** All new transactions are appended to the end of a log file, guaranteeing rapid write speeds without locking or reorganizing data.
2. **In-Memory Hash Index:** As records are written, their exact disk **byte-offset** is mapped to a RAM-based hash table.
3. **O(1) Direct Seeks:** Retrieval completely bypasses line-by-line scanning. The engine instantly jumps to the exact byte location on the hard drive using OS-level `seek()` operations.

##Performance Benchmark

Tested against a synthetic dataset of **100,000 JSON transaction records**:
*   **Standard Sequential Scan:** ~0.416 seconds
*   **Hash-Indexed Seek (This Engine):** ~0.000094 seconds
*   **Result:** Reduced worst-case query latency by **>99.9%**.



# CLI Commands
[1] Search ID - Instantly fetch a JSON payload by its Transaction ID.

[2] Insert New - Append a new transaction to the disk and dynamically update the RAM index.

[3] Exit - Gracefully shut down the server.

# Tech Stack & Constraints
Language: Python 3.x

Libraries: Pure Python Standard Library (os, json, time, random)

Constraints: Strictly obeyed constraints to use primitive data structures without specialized modules (like Pandas/NumPy) to demonstrate core computer science I/O and data structure fundamentals.
