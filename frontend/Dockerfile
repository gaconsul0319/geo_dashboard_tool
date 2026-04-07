# 1. 土台となるNode.jsの環境を用意します
FROM node:18-alpine

# 2. サーバーの中での作業場所を /app に決めます
WORKDIR /app

# 3. 持ち物リスト（package.jsonなど）をコピーします
COPY package*.json ./

# 4. パッケージをインストールします
RUN npm install

# 5. フロントエンドのプログラム本体をすべてコピーします
COPY . .

# 6. 本番用にファイルを最適化（ビルド）します
RUN npm run build

# 7. 完成した画面を配信するための軽量サーバー(serve)を準備します
RUN npm install -g serve

# 8. Cloud Run（サーバー）が動くときに実行するコマンドです（ポート8080で配信）
CMD ["serve", "-s", "dist", "-l", "8080"]