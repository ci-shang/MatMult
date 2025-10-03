# 1. Imports
import sys

import numpy as np
from Pyfhel import Pyfhel
from Arr_Processing import *
from data_process import *

print("\n1. Pyfhel Import")

# 2. BGV context and key setup
HE = Pyfhel()

bfv_params = {
    'scheme': 'BFV',
    'n': 2 ** 13,
    't': 65537,
    't_bits': 30,
    'sec': 128
}

HE.contextGen(**bfv_params)   # Generate context for bgv scheme
HE.keyGen()                   # Key Generation: generates a pair of public/secret keys
HE.rotateKeyGen()             # Rotate key generation --> Allows rotation/shifting
HE.relinKeyGen()              # Relinearization key generation

print("\n2. Pyfhel FHE context generation")
print(f"\t{HE}")

# 3. Processing Matrix
def processing_mat(A, B):
    # Padding Matrix
    mat_A, mat_B = padding_zero(A, B)

    print("\n3. Processing Matrix")
    print(f"->\tPadding Matrix A: \n{mat_A}")
    print(f"->\tPadding Matrix B: \n{mat_B}")
    d_A = mat_A.shape[0]
    d_B = mat_B.shape[0]

    # Binary vector
    binary_vec_A, arr_diag_flat = diag_masking_A(d_A, mat_A)
    arr_B = arr_B_extra(mat_B)

    return binary_vec_A, arr_diag_flat, arr_B

# 4. Integer 2-D Array and Vector Encoding & Encryption
def encryption(arr_diag_flat, arr_B):
    ptxt_A = HE.encodeInt(arr_diag_flat)
    ctxt_arr_A = HE.encryptPtxt(ptxt_A)

    # 提取出滚动后的每一个数组，并分别进行加密
    ctxt_arr_B = []
    for i in range(arr_B.shape[0]):
        ptxt_B = HE.encodeInt(arr_B[i])
        ctxt_B = HE.encryptPtxt(ptxt_B)
        ctxt_arr_B.append(ctxt_B)

    print("\n4. Integer Array Encoding & Encryption ")
    print("->\tarr_A ", arr_diag_flat, '\n\t==> ctxt_arr_A ', ctxt_arr_A)
    print("->\tarr_B \n", arr_B, '\n\t==> ctxt_arr_B ', ctxt_arr_B)
    return ctxt_arr_A, ctxt_arr_B

def encryption_runtime(arr_diag_flat, arr_B):
    ptxt_A = HE.encodeInt(arr_diag_flat)
    ctxt_arr_A = HE.encryptPtxt(ptxt_A)

    ptxt_B = HE.encodeInt(arr_B[0])
    ctxt_arr_B = HE.encryptPtxt(ptxt_B)

# 5. Compute two Matrixs Mul
def mat_mul_mat(ctxt_arr_A, binary_vec_A, ctxt_arr_B):
    arr_A_mul_binary = []
    for i in range(binary_vec_A.shape[0]):
        arr_A_mul_binary.append(ctxt_arr_A * binary_vec_A[i])
        arr_A_mul_binary[i] = arr_A_mul_binary[i] << (binary_vec_A.shape[0] * i)
    arr_A_mul_binary = np.array(arr_A_mul_binary)

    # Replicate arr_A element
    ctxt_arr_A = []
    for i in range(arr_A_mul_binary.shape[0]):
        arr_A = np.zeros((binary_vec_A.shape[0]), dtype=np.int64)
        arr_A_encode = HE.encodeInt(arr_A)
        for j in range(binary_vec_A.shape[0]):
            arr_A_encode = arr_A_encode + arr_A_mul_binary[i]
            arr_A_mul_binary[i] = arr_A_mul_binary[i] >> binary_vec_A.shape[0]
        ctxt_arr_A.append(arr_A_encode)
    ctxt_arr_A = np.array(ctxt_arr_A)
    # for i in range(len(ctxt_arr_A)):
    #     c_A = HE.decryptInt(ctxt_arr_A[i])
    #     print(c_A)

    # Merge arr_A element & Merge arr_B element
    arr_A_merge = ctxt_arr_A[0]
    arr_B_merge = ctxt_arr_B[0]
    for i in range(1, binary_vec_A.shape[0]):
        ctxt_arr_A[i] = ctxt_arr_A[i] >> (binary_vec_A.shape[0] ** 2) * i
        arr_A_merge  = arr_A_merge + ctxt_arr_A[i]

        ctxt_arr_B[i] = ctxt_arr_B[i] >> (binary_vec_A.shape[0] ** 2) * i
        arr_B_merge  = arr_B_merge + ctxt_arr_B[i]
    # a_A = HE.decryptInt(arr_A_merge)
    # for i in range(len(a_A)):
    #     print(a_A[i])

    mul_result = arr_A_merge * arr_B_merge
    ~mul_result

    # Divide Matrix & Add matrix
    # 1.Generate Binary vector
    bin_vec = []
    arr_len = len(ctxt_arr_B) ** 3
    d = len(ctxt_arr_B) ** 2
    i = 0
    while i < arr_len:
        temp = [0] * arr_len
        temp[i:i+d] = [1] * d
        bin_vec.append(temp)
        i = i + d

    # 2. Generate sub-matrix
    sub_matrix = []
    for i in range(len(bin_vec)):
        sub_matrix.append(mul_result * bin_vec[i])

    # 3. Rotate sub-matrix
    for i in range(1, len(sub_matrix)):
        sub_matrix[i] = sub_matrix[i] << (binary_vec_A.shape[0] ** 2) * i

    # 4. Add sub-matrix
    add_mul_result = np.zeros(len(ctxt_arr_B) ** 3, dtype=np.int64)
    result = HE.encodeInt(add_mul_result)
    for i in range(len(sub_matrix)):
        result += sub_matrix[i]

    print("\n5. Matrix multi matrix")
    print(f"\t==> Ciphertext result {result}")
    return result


if __name__ == '__main__':
    # A = np.random.randint(1, 100, size=(5, 8))
    # B = np.random.randint(100, 1000, size=(8, 9))
    A = np.array([[22, 34], [45, 89], [99, 37]], dtype=np.int64)
    B = np.array([[13, 36, 73, 83], [25, 46, 72, 92]], dtype=np.int64)

    # A = adult_process(2, 4)
    # B = adult_process(4, 5)

    # A = winequality_process(6, 12)
    # B = winequality_process(12, 12)

    # A = communities_process(20, 18)
    # B = communities_process(18, 16)

    binary_vec_A, arr_diag_flat, arr_B = processing_mat(A, B)

    # 计算encryption函数运行的时间
    ctxt_arr_A, ctxt_arr_B = encryption(arr_diag_flat, arr_B)
    ctxt_arr_A_size = sys.getsizeof(ctxt_arr_A)
    print(f"   - Size of ctxt_arr_A:           --> {ctxt_arr_A_size} ")

    temp_enc = running_time(encryption_runtime)
    temp_enc(arr_diag_flat, arr_B)

    # 计算mat_mul_mat函数的运行时间
    temp_mul = running_time(mat_mul_mat)
    mmm_result= temp_mul(ctxt_arr_A, binary_vec_A, ctxt_arr_B)
    # mmm_result = mat_mul_mat(ctxt_arr_A, binary_vec_A, ctxt_arr_B)

    # 计算decryption函数的运行时间
    dimension = binary_vec_A.shape[0]
    temp_dec = running_time(HE.decryptInt)
    matrix_mul_mat_result = temp_dec(mmm_result)
    # matrix_mul_mat_result = HE.decryptInt(mmm_result)

    mul_arr = matrix_mul_mat_result[:dimension ** 3]  # 解密后的明文取数组维度的平方个元素，且为一维数组

    mul_arr.resize((dimension ** 2, dimension))    # 将一维数组变成二维数组
    mul_arr = mul_arr.T      # 结果进行转置
    mul_arr = mul_arr[mul_arr != 0]   # 使用非0元素索引函数获取所有非0元素
    mul_arr.resize((A.shape[0], B.shape[1]))  # 最终的乘积数组维度为第一个数组的行数和第二个数组的列数
    print(f"\n\t==> HE Maritx and Mat Multi result: \n{mul_arr}")



