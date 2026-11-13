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
    return {"平均数":float(average),#便于JSON序列化
            "最大值":float(max_value),
            "最小值":float(min_value),
            "总和":float(sum_value)}

def group_by_column(df,group_column,value_column):
    if group_column not in df.columns:
        raise ValueError(f"列{group_column}不存在")
    if value_column not in df.columns:
        raise ValueError(f"列{value_column}不存在")
    grouped=df.groupby(group_column)[value_column].sum()
    return grouped.to_dict()#返回值从Series转换为字典，后续交给AI模型组织结果更方便

def get_top_n(df,column,n=5):
    if column not in df.columns:
        raise ValueError(f"列{column}不存在")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"列{column}不是数值类型")
    if not isinstance(n,int) or isinstance(n,bool) or n<=0:
        raise ValueError(f"n必须是正整数")
    top_n=df.sort_values(by=column,ascending=False).head(n)
    return top_n.to_dict(orient="records")