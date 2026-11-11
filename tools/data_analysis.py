import pandas as pd
def get_data_overview(df):
    overview={
        "行数":df.shape[0],
        "列数":df.shape[1],
        "列名":df.columns.tolist(),
        "数据类型":df.dtypes.astype(str).to_dict(),
        "缺失值数量":df.isnull().sum().to_dict()
        }
    return overview

def calculate_column_stats(df,column):
    if column not in df.columns:
        raise ValueError(f"列{column}不存在")
    #
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"列{column}不是数值类型")
    average=df[column].mean()
    max_value=df[column].max()
    min_value=df[column].min()
    sum_value=df[column].sum()
    return {"平均数":average,
            "最大值":max_value,
            "最小值":min_value,
            "总和":sum_value}