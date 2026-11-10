def get_data_overview(df):
    overview={
        "行数":df.shape[0],
        "列数":df.shape[1],
        "列名":df.columns.tolist(),
        "数据类型":df.dtypes.astype(str).to_dict(),
        "缺失值数量":df.isnull().sum().to_dict()
        }
    return overview