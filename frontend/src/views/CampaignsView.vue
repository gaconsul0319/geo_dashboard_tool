<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios' 

const router = useRouter()

// ←↓↓ ここを追加：アップロード画面へ移動する関数
const goToUpload = () => {
  router.push('/upload')
}

// 最初は箱を空っぽにしておきます
const campaigns = ref([])

// 英語のステータスを日本語に翻訳する辞書機能
const translateStatus = (status) => {
  switch (status) {
    case 'completed': return '完了'
    case 'processing': return '処理中'
    case 'waiting': return '待機中'
    case 'error': return 'エラー'
    default: return '待機中'
  }
}

// バックエンドの「受付窓口」にデータを取りに行く関数
const fetchCampaigns = async () => {
  try {
    // さっき作ったFastAPIの窓口（ポート8000番）にリクエストを送る
    const response = await axios.get('http://127.0.0.1:8000/api/jobs')
    
    if (response.data.status === 'success') {
      // バックエンドから届いたデータを、画面に表示しやすい形に変換して箱（campaigns）に入れる
      campaigns.value = response.data.data.map(job => ({
        id: job.id,
        name: job.filename,
        status: translateStatus(job.status),
        adid: job.id_count.toLocaleString(), // 1000のようにカンマ区切りにする
        progress: job.status === 'completed' ? '100%' : '処理待ち',
        date: job.upload_time ? new Date(job.upload_time).toLocaleString('ja-JP') : '不明',
        owner: 'テストユーザー' // 担当者は後でログイン機能と繋げます
      }))
      console.log("データの取得に成功しました！", campaigns.value)
    }
  } catch (error) {
    console.error("データの取得に失敗しました:", error)
  }
}

// 画面が開いた瞬間に、上の「fetchCampaigns」を実行するお約束
onMounted(() => {
  fetchCampaigns()
})

// 削除ボタンが押された時の処理
const deleteCampaign = async (id, name) => {
  // 1. 誤操作防止の確認ダイアログを出す
  if (!window.confirm(`本当に「${name}」を削除しますか？\n※この操作は取り消せません。`)) {
    return // 「キャンセル」が押されたらここで処理をストップ
  }

  try {
    // 2. バックエンドの「削除用窓口」にIDを送って削除をお願いする
    const response = await axios.delete(`http://127.0.0.1:8000/api/jobs/${id}`)
    
    if (response.data.status === 'success') {
      alert("削除が完了しました！")
      // 3. 削除が成功したら、もう一度リストを取り直して画面を最新にする
      fetchCampaigns()
    }
  } catch (error) {
    console.error("削除エラー:", error)
    alert("削除に失敗しました...")
  }
}

// ステータスによってバッジの色を変える関数（これはそのまま！）
const getStatusClass = (status) => {
  switch (status) {
    case '完了': return 'bg-green-100 text-green-700'
    case '処理中': return 'bg-blue-100 text-blue-700'
    case '待機中': return 'bg-yellow-100 text-yellow-700'
    case 'エラー': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <h1 class="text-2xl font-bold text-gray-800">案件管理</h1>
      <span class="text-sm text-gray-500 font-medium">キャンペーン一覧・管理</span>
    </div>

    <div class="flex space-x-4 bg-white p-4 rounded-xl shadow-sm border border-gray-100">
      <div class="flex-1 relative">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">🔍</span>
        <input type="text" placeholder="案件名で検索..." class="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
      </div>
      <select class="border rounded-lg px-4 py-2 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option>全状態</option>
        <option>完了</option>
        <option>処理中</option>
        <option>待機中</option>
        <option>エラー</option>
      </select>
      <button @click="goToUpload" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-blue-700 transition">
        ＋ 新規案件作成
      </button>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <table class="min-w-full text-sm text-left">
        <thead class="bg-gray-50 border-b text-gray-600">
          <tr>
            <th class="px-6 py-3 font-semibold">案件名</th>
            <th class="px-6 py-3 font-semibold">ステータス</th>
            <th class="px-6 py-3 font-semibold">ADID数</th>
            <th class="px-6 py-3 font-semibold">処理進捗</th>
            <th class="px-6 py-3 font-semibold">投入日時</th>
            <th class="px-6 py-3 font-semibold">担当</th>
            <th class="px-6 py-3 font-semibold text-center">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y text-gray-700">
          <tr v-for="campaign in campaigns" :key="campaign.id" class="hover:bg-gray-50 transition">
            <td class="px-6 py-4 font-medium">{{ campaign.name }}</td>
            <td class="px-6 py-4">
              <span :class="['px-2 py-1 rounded text-xs font-bold', getStatusClass(campaign.status)]">
                {{ campaign.status }}
              </span>
            </td>
            <td class="px-6 py-4">{{ campaign.adid }}</td>
            <td class="px-6 py-4 text-gray-500">{{ campaign.progress }}</td>
            <td class="px-6 py-4 text-gray-500">{{ campaign.date }}</td>
            <td class="px-6 py-4 text-gray-500">{{ campaign.owner }}</td>
            <td class="px-6 py-4 text-center space-x-3">
              <button class="text-blue-600 hover:text-blue-800 font-medium">詳細</button>
              <button class="text-blue-600 hover:text-blue-800 font-medium">地図</button>
              <button @click="deleteCampaign(campaign.id, campaign.name)" class="text-red-500 hover:text-red-700 font-medium">削除</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div class="px-6 py-3 border-t bg-gray-50 text-xs text-gray-500 flex justify-between items-center">
        <span>1-6 / 42件表示</span>
        <div class="space-x-1">
          <button class="px-2 py-1 border rounded bg-white hover:bg-gray-100">&lt;</button>
          <button class="px-2 py-1 border rounded bg-white hover:bg-gray-100">&gt;</button>
        </div>
      </div>
    </div>
  </div>
</template>