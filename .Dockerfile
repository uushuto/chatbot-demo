# ベースイメージを指定
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .
COPY step4.py .

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# スクリプトをデフォルトのコマンドとして設定
CMD ["python", "step4.py"]
