import openai

api_key = "sk-9902f39dd0694a769df2b94d851643d8"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

client = openai.OpenAI(api_key=api_key,base_url=base_url)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是哪家平台的大模型？并告诉我你的明确模型型号"}
    ]
)
print(response)