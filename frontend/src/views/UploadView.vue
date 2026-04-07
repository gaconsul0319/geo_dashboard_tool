<script setup>
import { ref } from 'vue';
import api from '../api'

// 状態管理用の変数
const selectedFile = ref(null);
const fileName = ref('');
const isUploading = ref(false);
const uploadMessage = ref('');

// ファイルが選択された時の処理
const handleFileSelect = (e) => {
  if (e.target.files.length > 0) {
    selectedFile.value = e.target.files[0];
    fileName.value = selectedFile.value.name;
    // 【ログ】ファイル選択時
    console.log(`[FileSelected] 選択されたファイル: ${fileName.value} (${selectedFile.value.size} bytes)`);
  }
};

// アップロード（送信）ボタンが押された時の処理
// アップロード（送信）ボタンが押された時の処理
const handleUpload = async () => {
  if (!selectedFile.value) {
    alert('CSVファイルを選択してください。');
    return;
  }
  
  isUploading.value = true;
  uploadMessage.value = 'アップロード準備中...';

  const file = selectedFile.value;
  // 38MBなどの巨大ファイルを「5MB」のブロックに切り分ける設定
  const CHUNK_SIZE = 5 * 1024 * 1024; 
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);

  try {
    let finalResponse = null;

    // ブロックの数だけ送信を繰り返す
    for (let i = 0; i < totalChunks; i++) {
      const start = i * CHUNK_SIZE;
      const end = Math.min(start + CHUNK_SIZE, file.size);
      const chunk = file.slice(start, end); // ファイルを切り取る

      // 送信用の箱（FormData）に、切り取ったパーツと「何番目のパーツか」の情報を入れる
      const formData = new FormData();
      formData.append('file', chunk);
      formData.append('filename', file.name);
      formData.append('chunkIndex', i);
      formData.append('totalChunks', totalChunks);

      uploadMessage.value = `送信中... (${i + 1}/${totalChunks})`;
      console.log(`[Upload] チャンク ${i + 1}/${totalChunks} を送信中...`);

      // バックエンドへ送信
      finalResponse = await api.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    }

    // すべてのパーツの送信が終わった時の処理
    console.log('[UploadSuccess] サーバーからのレスポンス:', finalResponse.data);
    uploadMessage.value = finalResponse.data.message;
    alert(`アップロード成功: ${finalResponse.data.message}`);
    
  } catch (error) {
    // 【ログ】エラー発生時
    console.error('[UploadError] 通信に失敗しました:', error);
    uploadMessage.value = 'エラーが発生しました。コンソールを確認してください。';
    alert('エラーが発生しました。詳細はブラウザのコンソール(F12)を確認してください。');
  } finally {
    isUploading.value = false;
  }
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <h1 class="text-2xl font-bold text-gray-800">CSVアップロード</h1>
      <span class="text-sm text-gray-500 font-medium">ADIDファイルアップロード</span>
    </div>

    <div class="bg-white p-10 rounded-xl shadow-sm border-2 border-dashed border-gray-300 hover:border-blue-500 transition text-center cursor-pointer relative group">
      <input type="file" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" @change="handleFileSelect" accept=".csv">
      
      <div class="space-y-4">
        <div class="text-6xl text-blue-500 group-hover:scale-110 transition transform duration-200">☁️</div>
        <h3 class="text-xl font-bold text-gray-700">CSVファイルをドラッグ＆ドロップ</h3>
        <p class="text-gray-500">または クリックしてファイルを選択</p>
        <div class="bg-gray-50 p-3 rounded-lg inline-block mt-4">
          <p class="text-xs text-gray-500 text-left leading-relaxed">
            • 対応形式: CSV（IDFA / AAID / SHA-256ハッシュ）<br>
            • 件数制限なし（数件〜数百万件対応）｜GB級はGCS直接アップロード
          </p>
        </div>
        <p v-if="fileName" class="text-blue-600 font-bold mt-4 bg-blue-50 py-2 rounded">選択中のファイル: {{ fileName }}</p>
      </div>
    </div>

    <p v-if="uploadMessage" class="text-center text-sm font-bold" :class="isUploading ? 'text-blue-600' : 'text-green-600'">
      {{ uploadMessage }}
    </p>

    <div class="flex flex-col items-center space-y-3">
      <button 
        @click="handleUpload"
        :disabled="isUploading || !selectedFile"
        class="bg-blue-600 text-white px-12 py-4 rounded-full text-lg font-bold hover:bg-blue-700 disabled:bg-gray-400 transition shadow-lg w-full max-w-md flex justify-center items-center space-x-2"
      >
        <span>{{ isUploading ? '処理中...' : '送信（非同期・離脱可能）' }}</span>
      </button>
      <p class="text-sm text-gray-500 flex items-center">
        <span class="mr-1">ℹ️</span> 送信後、ブラウザを閉じても処理は継続します（Firestore永続管理）
      </p>
    </div>

    <div class="grid grid-cols-2 gap-6 pt-4">
      
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-lg font-bold text-gray-800 mb-5 border-b pb-2">アップロード設定</h2>
        
        <div class="space-y-5">
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">案件名（キャンペーン名）</label>
            <input type="text" placeholder="例: 春キャンペーン_東京" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition">
          </div>
          
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">ID形式</label>
              <select class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition">
                <option>IDFA / AAID</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-bold text-gray-700 mb-1">ハッシュ化</label>
              <select class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition">
                <option>なし（生ID）</option>
                <option>SHA-256</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-bold text-gray-700 mb-1">計測地点POI</label>
            <select class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition mb-2">
              <option>店舗マスターから選択</option>
              <option>渋谷店</option>
              <option>新宿店</option>
            </select>
            <p class="text-xs text-gray-500 mb-1 mt-3">または 緯度・経度を直接入力</p>
            <input type="text" placeholder="35.6812, 139.7671" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:bg-white focus:ring-2 focus:ring-blue-500 outline-none transition text-sm">
          </div>
        </div>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-lg font-bold text-gray-800 mb-5 border-b pb-2">バリデーション結果</h2>
        
        <div class="space-y-3">
          <div class="flex items-center space-x-3 text-green-700 bg-green-50 p-3 rounded-lg border border-green-100">
            <span class="text-lg">✅</span>
            <p class="text-sm font-bold">ファイル形式: CSV — OK</p>
          </div>
          <div class="flex items-center space-x-3 text-green-700 bg-green-50 p-3 rounded-lg border border-green-100">
            <span class="text-lg">✅</span>
            <p class="text-sm font-bold">ファイル非空: 520,340行 — OK</p>
          </div>
          <div class="flex items-center space-x-3 text-green-700 bg-green-50 p-3 rounded-lg border border-green-100">
            <span class="text-lg">✅</span>
            <p class="text-sm font-bold">列名検証: adid列存在 — OK</p>
          </div>
          <div class="flex items-start space-x-3 text-yellow-700 bg-yellow-50 p-3 rounded-lg border border-yellow-200 mt-4">
            <span class="text-lg mt-0.5">⚠️</span>
            <div>
              <p class="text-sm font-bold">残高チェック: 残ID数 16,470,000 >= 520,340 — OK（通過）</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>