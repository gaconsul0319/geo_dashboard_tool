import axios from 'axios';

// バックエンド（FastAPI）と通信するための専用設定を作成
const api = axios.create({
  // .envファイルに書いたURL（VITE_API_BASE_URL）を自動で読み込む
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;