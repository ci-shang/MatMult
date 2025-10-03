import numpy as np
import time

def padding_zero(A, B):
    row_A, col_A = A.shape
    row_B, col_B = B.shape
    m = max(row_A, row_B, col_A, col_B)  
    n = max(col_A, col_B, row_A, row_B)  

    A_padded = [[0] * n for _ in range(m)] 
    B_padded = [[0] * n for _ in range(m)]

    for i in range(row_A):
        for j in range(col_A):
            A_padded[i][j] = A[i][j]

    for i in range(row_B):
        for j in range(col_B):
            B_padded[i][j] = B[i][j]
    return np.array(A_padded), np.array(B_padded)

def diagonal(arr):
    d = arr.shape[0]
    arr_list = []
    # arr_list.append(np.diagonal(arr))
    for k in range(d):
        arr_list.append(np.diagonal(arr))
        arr = np.roll(arr, -1, axis=1)      
    return np.array(arr_list).flatten()     

def diag_masking_A(d, arr):
    arr_diag_flat = diagonal(arr)
    arr_len = arr_diag_flat.shape[0]
    binary_vec = []

    i = 0
    while i < arr_len:
        temp = [0] * arr_len
        temp[i:i+d] = [1] * d
        binary_vec.append(temp)
        i = i + d

    print("\nGenerate binary vector for A")
    print("->\tarr_diag_flat: ", arr_diag_flat)
    print(f"->\t{np.array(binary_vec)}")
    return np.array(binary_vec), arr_diag_flat

def arr_B_extra(arr):
    arr = arr.T
    arr_B = []
    for i in range(arr.shape[0]):
        arr_B.append(np.roll(arr, -i, axis=1)) 
        arr_B[i] = arr_B[i].flatten()

    # binary_vec = np.where(arr_flat != 0, 1, 0)

    print("\nExtraction array B element and roll......")
    # print(f"\tarr_B: {arr_B}")
    # print(f"\t{binary_vec}")
    # return np.array(arr_B).flatten()
    return np.array(arr_B)

def running_time(f, c = 1):
    # function cost time
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        clock_time = time2 - time1
        if c == 0:
            return clock_time
        else:
            print(f"\t==> {f.__name__} function took {clock_time * 1000.0: 0.3f}ms")
            return ret
    return wrap

if __name__ == '__main__':
    A = np.array([[1, 2], [3, 4], [5, 6]])
    B = np.array([[5, 6, 7], [8, 9, 10]])
    A_padded, B_padded = padding_zero(A, B)
    print(A_padded)
    print(B_padded)

    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int64)
    diag_arr = diagonal(arr)
    print(diag_arr)


    binary_vec, arr_diag_flat = diag_masking_A(arr.shape[0], arr)
    arr_B = arr_B_extra(B_padded)
    print(arr_B)


