import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from main import load_data
from tools.data_analysis import*

load_dotenv()  # 加载 .env 文件中的环境变量
client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_data_overview",
            "description": "查看数据集的基本信息，包括行数、列数、列名、数据类型和缺失值数量",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_column_stats",
            "description": "计算指定数值列的平均值、最大值、最小值和总和",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "需要进行统计的列名"
                    }
                },
                "required": ["column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "group_by_column",
            "description": "按照指定列进行分组，并计算另一数值列的总和",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_column": {
                        "type": "string",
                        "description": "用于分组的列名"
                    },
                    "value_column": {
                        "type": "string",
                        "description": "需要计算总和的数值列名"
                    }
                },
                "required": ["group_column", "value_column"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_n",
            "description": "按照指定数值列降序排列，返回数值最大的前N条记录",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "用于排序的数值列名"
                    },
                    "n": {
                        "type": "integer",
                        "description": "需要返回的记录数量，默认5"
                    }
                },
                "required": ["column"]
            }
        }
    }
]
available_functions = {
    "get_data_overview": get_data_overview,
    "calculate_column_stats": calculate_column_stats,
    "group_by_column": group_by_column,
    "get_top_n": get_top_n
}

def ask_model(messages):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        extra_body={"thinking": {"type": "disabled"}}
    )

    message = response.choices[0].message

    return message

def execute_function(tool_call, df):
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    function_to_call = available_functions[function_name]

    result = function_to_call(df, **function_args)

    return result

if __name__ == "__main__":
    df = load_data("data/sales.csv")

    messages=[
            {
                "role": "system",
                "content": """
你是一个数据分析助手，请根据用户的具体需求选择工具。

工具选择规则：
1. 用户询问数据集有多少行、多少列、有哪些字段、缺失值等整体信息时，使用 get_data_overview。
2. 用户询问某个数值列的平均值、最大值、最小值或总和时，使用 calculate_column_stats。
3. 用户要求按照某一列分组，并统计另一列的总和时，使用 group_by_column。
4. 用户要求找出某个数值列排名前N的记录时，使用 get_top_n。

请准确选择与用户需求对应的工具，不要把整体数据概览工具用于具体数值统计问题。
"""
            }, {
                "role": "user",
                "content": "帮我找出销售额最高的三条记录"
            }]

    message = ask_model(messages)

if message.tool_calls:

    messages.append(message)

    for tool_call in message.tool_calls:
        print("模型选择的工具：", tool_call.function.name)
        print("模型提供的参数：", tool_call.function.arguments)

        result = execute_function(tool_call, df)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False, default=str)
        })

    final_message = ask_model(messages)

    print("AI 最终回答：")
    print(final_message.content)

else:
    print("模型回答：", message.content)
