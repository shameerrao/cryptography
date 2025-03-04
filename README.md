# Cryptography Algorithms

This repository contains simple, educational implementations of some of the most commonly used cryptographic algorithms. These implementations aim to demonstrate the inner workings of each algorithm but **should not** be used in production environments, as they are not designed with security in mind and may be vulnerable to known attacks.

## Algorithms Implemented

### 1. **Data Encryption Standard (DES)**
A well-known symmetric-key block cipher that has been widely used in the past but is now considered insecure for most purposes.

### 2. **Diffie-Hellman Key Exchange**
An essential public-key cryptography algorithm used to securely exchange cryptographic keys over a public channel. It's foundational for protocols like IPsec, TLS, and SSH.

### 3. **Feistel Cipher**
A structure used in many block ciphers, including DES. The Feistel cipher divides the data block into two halves and processes them iteratively in rounds.

### 4. **RC4**
A stream cipher that has been widely used in various protocols like WPA, WEP, and TLS/SSL. It is now considered weak due to vulnerabilities discovered over time.

### 5. **Vigenère and Caesar Ciphers**
Elementary and easy-to-understand ciphers used for text-based encryption. They are often used as teaching tools to introduce basic concepts of cryptography.

## **Disclaimer**
These implementations are **not** suitable for use in production systems. They are for educational purposes only, intended to help users understand how these algorithms work internally.
