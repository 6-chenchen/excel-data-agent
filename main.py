import pandas as pd
from pathlib import Path
from tools.data_analysis import get_data_overview
def load_data(file_path):
    """
    读取 CSV 或 Excel 文件。

    参数：
        file_path: 文件路径

    返回：
        df: Pandas DataFrame 数据表
    """

    path = Path(file_path)

    # 判断文件类型suffix 后缀 prefix前缀
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)

    elif path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)

    else:
        raise ValueError("暂不支持该文件格式")

    # 输出数据基本信息
    print("========== 数据读取成功 ==========")
    print("数据规模：", df.shape)

    print("\n字段名称：")
    print(df.columns.tolist())

    print("\n数据类型：")
    print(df.dtypes)

    print("\n数据预览：")
    print(df.head())

    return df


if __name__ == "__main__":
    
    file_path = "data/sales.csv"
    data = load_data(file_path)
    result=get_data_overview(data)
    print("\n数据概览：")
    print(result)
