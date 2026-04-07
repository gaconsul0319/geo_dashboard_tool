# 1. 土台となるPythonの環境（バージョン3.10）を用意します
FROM python:3.10-slim

# 2. サーバーの中での作業場所（ディレクトリ）を /app に決めます
WORKDIR /app

# 3. 先ほど作った「持ち物リスト」をサーバーにコピーします
COPY requirements.txt .

# 4. 持ち物リストに書いてあるパッケージをインストールします
RUN pip install --no-cache-dir -r requirements.txt

# 5. バックエンドのプログラム本体（main.pyなど）をすべてコピーします
COPY . .

# 6. Cloud Run（サーバー）が動くときに実行するコマンド（起動スイッチ）です
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]