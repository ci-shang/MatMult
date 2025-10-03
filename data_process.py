import pandas as pd
import numpy as np

def adult_process(row_shape, col_shape):
    # x is dataset's rows
    columns = ['Age','Workclass','fnlgwt','Education','EdNum','MaritalStatus',
           'Occupation','Relationship','Race','Sex','CapitalGain',
           'CapitalLoss','HoursPerWeek','Country','Income']

    data = pd.read_csv('data/adult.csv', names=columns)

    # 选择连续型的数据列
    continuous_cols = []

    for col in data.columns:
        if data[col].dtype != 'object':
            continuous_cols.append(col)

    continuous_data = data[continuous_cols]

    adult_arr = continuous_data.values

    adult_rows = np.random.choice(adult_arr.shape[0], size=row_shape, replace=False)
    adult_cols = np.random.choice(adult_arr.shape[1], size=col_shape, replace=False)

    return adult_arr[adult_rows][:, adult_cols]

def winequality_process(row_shape, col_shape):

    data = pd.read_csv('data/winequality-white.csv', sep=';', header=0)

    winequality_arr = data.multiply(100).values.astype(int)

    wine_rows = np.random.choice(winequality_arr .shape[0], size=row_shape, replace=False)
    wine_cols = np.random.choice(winequality_arr .shape[1], size=col_shape, replace=False)

    return winequality_arr[wine_rows][:, wine_cols]

def communities_process(row_shape, col_shape):

    data = pd.read_csv('data/communities.csv', header=0)
    data = data.iloc[:, 31: 51]

    communities_arr = data.multiply(100).values.astype(int)

    communities_rows = np.random.choice(communities_arr .shape[0], size=row_shape, replace=False)
    communities_cols = np.random.choice(communities_arr .shape[1], size=col_shape, replace=False)

    return communities_arr[communities_rows][:, communities_cols]

if __name__ == '__main__':
    adult_mat = adult_process(4, 6)
    print(adult_mat)

    wine_mat = winequality_process(4, 6)
    print(wine_mat)

    communities_mat = communities_process(4, 6)
    print(communities_mat)
