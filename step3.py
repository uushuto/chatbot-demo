import os

import chainlit as cl
import openai
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# チャットが開始されたときに実行される関数
@cl.on_chat_start
async def start():
    # チャット開始時のメッセージを送信
    await cl.Message(content="こんにちは！どのようにお手伝いできますか？").send()

# ユーザーがメッセージを入力するたびに実行される関数
@cl.on_message
async def main(message: cl.Message):
    # OpenAI APIにリクエストを送信
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.content},  # message.content を使用してユーザーの入力を取得
        ]
    )
    
    # OpenAIからの返答を取得し、ユーザーに送信
    reply = response['choices'][0]['message']['content']
    await cl.Message(content=reply).send()
