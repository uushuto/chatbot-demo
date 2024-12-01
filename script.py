import os

from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()

# 環境変数からAPIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# APIキーが正しく読み込まれているか確認
print(api_key)