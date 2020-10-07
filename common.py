import pandas as pd


def analyze(df, dims):
    dicts = list()
    for name, row in df.iterrows():
        temp = dict()
        percent = row / row.sum()
        for dim, val in dims.iterrows():
            temp[dim] = sum(percent * val)
        dicts.append(temp)
    return pd.DataFrame(dicts, index=df.index)

