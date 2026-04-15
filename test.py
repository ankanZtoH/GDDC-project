from openai import OpenAI

client = OpenAI(
    api_key="sk-df83a5fd45464fcf8a69970f97958d8c",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)