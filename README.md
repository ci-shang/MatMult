# Homomorphic Encryption Matrix Operations with Pyfhel

This project demonstrates how to use [**Pyfhel**](https://github.com/ibarrond/Pyfhel), a Python library for fully homomorphic encryption (FHE), to perform encrypted matrix operations. It shows how to process data securely without decrypting it, with applications in **privacy-preserving matrix computation** and **secure data processing**.

---

## 📂 Project Structure

- **`data_process.py`**  
  Provides data pre-processing utilities for handling inputs. 

- **`arr_process.py`**  
  Implements basic array processing before encryption.  

- **`matrix_mult_matrix.py`**  
  Demonstrates **matrix multiplication** over encrypted data using Pyfhel.  
  It shows how homomorphic operations can be applied to matrix structures securely.    

---

## ⚙️ Installation

Make sure you have **Python 3.8+** installed.  
Install required dependencies:

```bash
pip install pyfhel
