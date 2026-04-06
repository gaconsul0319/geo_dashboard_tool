import { initializeApp } from "firebase/app";
// 新規追加：認証用の機能をインポート
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// スクリーンショットの設定値
const firebaseConfig = {
  apiKey: "AIzaSyCXGbbr4mRh_ZSZZdN9584J8hjeAz2_H7E",
  authDomain: "geo-viewer-app.firebaseapp.com",
  projectId: "geo-viewer-app",
  storageBucket: "geo-viewer-app.firebasestorage.app",
  messagingSenderId: "784967747441",
  appId: "1:784967747441:web:152bcc6be92252e2e498d0"
};

// Firebaseの初期化
const app = initializeApp(firebaseConfig);

// 新規追加：認証の初期化とGoogleログインの準備
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Googleのログイン画面を日本語で表示するための設定
auth.useDeviceLanguage();

// 他のファイルで使えるように書き出す
export { auth, provider };