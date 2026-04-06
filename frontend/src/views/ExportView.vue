<script setup>
import axios from 'axios'

// CSVダウンロードボタンが押されたときの処理
const downloadCsv = async () => {
  try {
    // 1. バックエンドの「CSVダウンロード窓口」にお願いする
    // ※ファイルをダウンロードするときは、responseTypeを 'blob'（データの塊）に設定します
    const response = await axios.get('http://127.0.0.1:8000/api/export/csv', {
      responseType: 'blob'
    })

    // 2. 受け取ったデータの塊から、ブラウザでダウンロードできる「URL」を作る
    const url = window.URL.createObjectURL(new Blob([response.data]))
    
    // 3. 透明な <a> タグ（リンク）を作って、自動でクリックさせる（＝ダウンロードが始まる）
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'analysis_data.csv') // ファイル名を指定
    document.body.appendChild(link)
    link.click()
    
    // 4. 後片付け（作ったリンクを消す）
    link.parentNode.removeChild(link)
    
    console.log("CSVのダウンロードに成功しました！")
  } catch (error) {
    console.error("ダウンロードエラー:", error)
    alert("ダウンロードに失敗しました...")
  }
}

const downloadImage = () => {
  // 本来はdeck.glのCanvasから画像を生成する、またはバックエンドに依頼する処理が入ります
  alert("【開発中】地図画像（PNG/JPEG）の出力機能は、次期アップデートで実装予定です。")
}


const downloadPdf = () => {
  // ブラウザの標準印刷（PDF保存）機能を暫定的に呼び出す
  if (window.confirm("【暫定機能】ブラウザの印刷機能を使用してPDFとして保存しますか？")) {
    window.print()
  }
}

</script>

<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <div class="flex items-center space-x-4">
        <h1 class="text-2xl font-bold text-gray-800">エクスポート</h1>
      </div>
      <div class="text-sm text-gray-500 font-medium">レポート出力形式を選択</div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 pt-4">
      
      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center space-y-6 hover:shadow-md transition">
        <div class="w-20 h-20 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-3xl">
          🗺️
        </div>
        <div>
          <h2 class="text-lg font-bold text-gray-800 mb-2">地図画像エクスポート</h2>
          <p class="text-xs text-gray-500 leading-relaxed">
            deck.glヒートマップ描画結果を画像として出力。プレゼン資料やクライアント報告書に最適。
          </p>
        </div>
        <div class="w-full pt-4">
          <select class="w-full mb-3 text-xs border rounded-lg px-3 py-2 bg-gray-50 outline-none focus:ring-1 focus:ring-blue-500">
            <option>形式: PNG (.png)</option>
            <option>形式: JPEG (.jpg)</option>
          </select>
          <button @click="downloadImage" class="w-full py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-sm transition">
            画像をダウンロード
          </button>
        </div>
      </div>

      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center space-y-6 hover:shadow-md transition">
        <div class="w-20 h-20 bg-green-50 text-green-600 rounded-full flex items-center justify-center text-3xl">
          📊
        </div>
        <div>
          <h2 class="text-lg font-bold text-gray-800 mb-2">分析データCSV</h2>
          <p class="text-xs text-gray-500 leading-relaxed">
            来訪UU数・回数・時間帯別等の生データをCSV出力。BigQuery等のDMPへの二次取込に対応。
          </p>
        </div>
        <div class="w-full pt-4">
          <select class="w-full mb-3 text-xs border rounded-lg px-3 py-2 bg-gray-50 outline-none focus:ring-1 focus:ring-green-500">
            <option>形式: CSV (.csv)</option>
          </select>
          <button @click="downloadCsv" class="w-full py-3 bg-green-600 text-white rounded-xl font-bold hover:bg-green-700 shadow-sm transition">
            CSVをダウンロード
          </button>
        </div>
      </div>

      <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 flex flex-col items-center text-center space-y-6 hover:shadow-md transition">
        <div class="w-20 h-20 bg-orange-50 text-orange-600 rounded-full flex items-center justify-center text-3xl">
          📄
        </div>
        <div>
          <h2 class="text-lg font-bold text-gray-800 mb-2">統合レポート (PDF)</h2>
          <p class="text-xs text-gray-500 leading-relaxed">
            エリア可視化＋来訪分析を統合したPDFレポート。案件サマリ・KPI・グラフを一括出力。
          </p>
        </div>
        <div class="w-full pt-4">
          <select class="w-full mb-3 text-xs border rounded-lg px-3 py-2 bg-gray-50 outline-none focus:ring-1 focus:ring-orange-500">
            <option>形式: PDF (.pdf)</option>
          </select>
          <button @click="downloadPdf" class="w-full py-3 bg-orange-600 text-white rounded-xl font-bold hover:bg-orange-700 shadow-sm transition">
            PDFをダウンロード
          </button>
        </div>
      </div>

    </div>

    <div class="mt-12 bg-gray-50 p-6 rounded-xl border border-gray-200">
      <h3 class="text-sm font-bold text-gray-700 mb-2 flex items-center">
        <span class="mr-2">🔗</span>DMP連携について
      </h3>
      <p class="text-xs text-gray-500 leading-relaxed">
        エクスポートしたCSVデータは、当社標準のDMP（BigQuery等）へ直接インポート可能なフォーマットで出力されます。API連携による自動取得を希望される場合は、システム管理者までお問い合わせください。[cite: 1730, 2030]
      </p>
    </div>

  </div>
</template>