# Homomorphic Encryption Matrix Operations with Pyfhel

This project demonstrates how to use [**Pyfhel**](https://github.com/ibarrond/Pyfhel), a Python library for homomorphic encryption (HE), to perform encrypted array and matrix operations.  
The scripts show how to process data securely without decrypting it, with applications in **privacy-preserving matrix computation** and **secure data processing**.

---

## 📂 Project Structure

- **`arr_process.py`**  
  Implements basic encrypted array processing (encryption, decryption, element-wise operations, etc.).  

- **`Matrix_mul_matrix.py`**  
  Demonstrates **matrix multiplication** over encrypted data using Pyfhel.  
  It shows how homomorphic operations can be applied to matrix structures securely.  

- **`data_process.py`**  
  Provides data pre-processing utilities for handling inputs before encryption,  
  and post-processing after decryption.  

---

## ⚙️ Installation

Make sure you have **Python 3.8+** installed.  
Install required dependencies:

```bash
pip install pyfhel
