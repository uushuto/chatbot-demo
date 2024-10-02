import chainlit as cl


# チャットが開始されたときに実行される関数
@cl.on_chat_start
async def main():
    # ローカルのPDFファイルをインラインで表示
    elements = [
      cl.Pdf(name="pdf1", display="inline", path="./ronbun.pdf")  # ローカルのPDFファイルのパスを指定
    ]

    # メッセージと共にPDFを表示
    await cl.Message(content="こちらのPDFをご覧ください！", elements=elements).send()
