
import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 读取 .env 文件
load_dotenv()

# 2. 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 API Key，请检查 .env 文件")

# 3. 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 4. 向模型发送请求
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍你自己。"}
    ]
)

# 5. 获取并打印模型回复
print(response.choices[0].message.content)
