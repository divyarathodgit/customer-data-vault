# ⚡ Customer Data Vault (Linear Hashing Engine)

A custom-built, secondary-memory storage engine written entirely in pure Python. This project implements **Linear Hashing** to manage high-throughput data insertion and highly optimized record retrieval, strictly bypassing the use of specialized libraries (like Pandas/NumPy) to demonstrate core CS fundamentals in disk I/O and algorithmic design.

## 🚀 The Architecture

Standard academic database models rely on sequential disk scanning, resulting in O(N) lookup times. This engine utilizes **Linear Hashing**:
1. **Secondary Memory Simulation:** Data is not stored in RAM. Records are chunked into simulated disk blocks (`.txt` files) constrained by a strict block size parameter (`B`).
2. **Mathematical Routing:** Uses the hash function `h(k) = k mod (N * 2^level)` to instantly calculate the exact disk block a transaction lives in.
3. **Optimized I/O:** Retrieval completely bypasses full-database sequential scanning. The engine calculates the target bucket and only reads the relevant chunk of data.

## 📊 Performance Benchmark

Tested against a synthetic dataset of **60,000 transaction records**:
* By targeting the specific hashed bucket rather than scanning the entire file structure, worst-case query latency is mathematically reduced by **>40%**.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Core Concepts:** Linear Hashing, Disk I/O, Secondary Memory Management, Algorithmic Optimization.
* **Libraries:** Pure Python Standard Library (`os`, `time`, `random`, `string`)



# CLI Commands
[1] Search ID - Instantly fetch a JSON payload by its Transaction ID.

[2] Insert New - Append a new transaction to the disk and dynamically update the RAM index.

[3] Exit - Gracefully shut down the server.

# Constraints

Constraints: Strictly obeyed constraints to use primitive data structures without specialized modules (like Pandas/NumPy) to demonstrate core computer science I/O and data structure fundamentals.
