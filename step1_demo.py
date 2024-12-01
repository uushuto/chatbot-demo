import os

import openai  # OpenAIライブラリをインポート
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI APIキーを設定
openai.api_key = api_key

# OpenAI APIへのリクエスト
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How are you?"},
    ]
)

# 返答を出力
print(response['choices'][0]['message']['content'])