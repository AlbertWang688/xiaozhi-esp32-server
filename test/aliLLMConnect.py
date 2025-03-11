# import openai

# api_key = "sk-9902f39dd0694a769df2b94d851643d8"
# base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# client = openai.OpenAI(api_key=api_key,base_url=base_url)

# response = client.chat.completions.create(
#     model="qwen-plus",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "你是哪家平台的大模型？并告诉我你的明确模型型号"}
#     ]
# )
# print(response)


# import datetime
from datetime import datetime

strTime1 = '2025-03-10T09:10:46.112Z'
strTime2 = '2025-03-10 09:10:46'
strTime3 = '2025-03-10'
# print(datetime.strptime(strTime3, '%Y-%m-%dT%H:%M:%S.%fZ'))
# 格式化strTime1为DateTime对象,并输出isoformat格式
time1 = datetime.fromisoformat(strTime3)
print("time1 type:",{type(time1)}, "  time1:", {time1.isoformat()})
