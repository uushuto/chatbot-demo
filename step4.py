import os

import chainlit as cl
import faiss
import numpy as np
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# 環境変数からAPIキーを読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FAISSの初期化
dimension = 1536  # OpenAI text-embedding-ada-002の次元数
index = faiss.IndexFlatL2(dimension)
document_store = []

@cl.on_chat_start
async def start():
    """
    チャット開始時にファイルアップロードを促す
    """
    files = await cl.AskFileMessage(
        content="解析したいPDFファイルをアップロードしてください。",
        accept=["application/pdf"],  # PDFファイルのみ許可
        max_size_mb=10  # 最大ファイルサイズを10MBに制限
    ).send()

    if not files:
        await cl.Message(content="ファイルがアップロードされませんでした。").send()
        return

    file = files[0]  # 最初のファイルを処理
    try:
        # アップロードされたファイルのパスを使用して内容を読み取る
        pdf_reader = PdfReader(file.path)  # 修正：file.content → file.path
        text = "\n".join([page.extract_text() for page in pdf_reader.pages])

        # テキストを段落に分割してインデックス化
        paragraphs = text.split("\n\n")
        for para in paragraphs:
            if para.strip():  # 空白行を無視
                embedding = openai.Embedding.create(
                    input=para, model="text-embedding-ada-002"
                )['data'][0]['embedding']
                index.add(np.array([embedding]))
                document_store.append(para)

        await cl.Message(content="ファイルを解析してインデックス化しました。質問をどうぞ！").send()
    except Exception as e:
        await cl.Message(content=f"ファイルの解析中にエラーが発生しました: {str(e)}").send()


@cl.on_message
async def answer_question(message):
    """
    ユーザーの質問に基づき関連する情報を検索し回答を生成
    """
    try:
        # 質問をベクトル化
        query_embedding = openai.Embedding.create(
            input=message.content, model="text-embedding-ada-002"
        )['data'][0]['embedding']

        # FAISSで関連ドキュメントを検索
        top_k = 5
        distances, indices = index.search(np.array([query_embedding]), top_k)

        # 上位の段落を取得
        context = "\n".join([document_store[idx] for idx in indices[0] if idx != -1])

        # ChatGPT APIで回答生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"以下の情報を基に質問に答えてください:\n{context}"},
                {"role": "user", "content": message.content}
            ]
        )

        # ユーザーに応答を送信
        await cl.Message(content=response['choices'][0]['message']['content']).send()
    except Exception as e:
        await cl.Message(content=f"エラーが発生しました: {str(e)}").send()
