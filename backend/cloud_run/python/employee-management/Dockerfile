# Python 3.11 slim をベースに使用
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なOSパッケージのインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 公式イメージから uv バイナリをコピーして高速インストールを可能にする
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 依存パッケージファイルをコピーしてインストール
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# アプリケーションソースコードをコピー
COPY . .

# ポートの公開（Cloud Run は環境変数 PORT で指定されるポートを監視）
ENV PORT=8000
EXPOSE 8000

# PYTHONPATH を設定して、ルートおよびパッケージ内からインポート可能にする
ENV PYTHONPATH=/app:/app/employee-management

# 起動コマンド（uvicornでFastAPIを起動）
CMD ["sh", "-c", "uvicorn employee_management.main:app --host 0.0.0.0 --port ${PORT} --reload"]
