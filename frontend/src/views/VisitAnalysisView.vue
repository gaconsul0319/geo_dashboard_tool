<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <div class="flex items-center space-x-4">
        <h1 class="text-2xl font-bold text-gray-800">来訪分析</h1>
        <div class="flex space-x-2">
          <select class="text-xs border rounded-lg px-2 py-1 bg-white text-gray-600 focus:outline-none focus:ring-1 focus:ring-blue-500">
            <option>計測地点: 渋谷店</option>
          </select>
          <select class="text-xs border rounded-lg px-2 py-1 bg-white text-gray-600 focus:outline-none focus:ring-1 focus:ring-blue-500">
            <option>期間: 過去30日</option>
          </select>
        </div>
      </div>
      <div class="bg-blue-50 px-3 py-1 rounded-full border border-blue-100">
        <p class="text-[10px] text-blue-600 font-bold flex items-center">
          <span class="mr-1">ℹ️</span> 滞在時間 5分以上（通過除外）
        </p>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 relative overflow-hidden">
        <div class="absolute top-0 right-0 p-3 opacity-10 text-3xl">👥</div>
        <p class="text-sm text-gray-500 font-medium mb-1">来訪UU数</p>
        <div class="flex items-baseline space-x-3">
          <p class="text-3xl font-bold text-gray-800">12,842</p>
          <span class="text-xs font-bold text-green-500">↑ 18.2%</span>
        </div>
        <p class="text-[10px] text-gray-400 mt-2">対前月比の成長率</p>
      </div>
      
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 relative overflow-hidden">
        <div class="absolute top-0 right-0 p-3 opacity-10 text-3xl">🔄</div>
        <p class="text-sm text-gray-500 font-medium mb-1">総来訪回数</p>
        <div class="flex items-baseline space-x-3">
          <p class="text-3xl font-bold text-gray-800">28,127</p>
          <span class="text-xs text-gray-400">1人平均 2.2回</span>
        </div>
        <p class="text-[10px] text-gray-400 mt-2">指定期間内の累計値</p>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 relative overflow-hidden">
        <div class="absolute top-0 right-0 p-3 opacity-10 text-3xl">⏱️</div>
        <p class="text-sm text-gray-500 font-medium mb-1">平均滞在時間</p>
        <div class="flex items-baseline space-x-3">
          <p class="text-3xl font-bold text-gray-800">22分</p>
          <span class="text-xs text-gray-400">中央値 17分</span>
        </div>
        <p class="text-[10px] text-gray-400 mt-2">1来訪あたりの平均時間</p>
      </div>
    </div>

    <div v-if="apiData" class="space-y-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-sm font-bold text-gray-800 mb-6">日別来訪UU推移（過去30日・滞在5分以上）</h2>
        <div>
          <LineChart :chartData="apiData.data.line_chart" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 class="text-sm font-bold text-gray-800 mb-6">時間帯別分布</h2>
          <div>
            <BarChart :chartData="apiData.data.hourly_bar_chart" />
          </div>
        </div>

        <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h2 class="text-sm font-bold text-gray-800 mb-6">曜日別分布</h2>
          <div>
            <WeeklyBarChart :chartData="apiData.data.weekly_bar_chart" />
          </div>
        </div>
      </div>
    </div>

    <div v-else class="space-y-6 flex justify-center items-center h-64">
      <p class="text-gray-500 font-bold animate-pulse">📊 データを裏側から取得中...</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios'; // フェーズ3で導入済みの、通信を行うための道具

// 3つのグラフコンポーネントを読み込む
import BarChart from '../components/BarChart.vue';
import LineChart from '../components/LineChart.vue';
import WeeklyBarChart from '../components/WeeklyBarChart.vue';

// データの入れ物を準備（最初は空っぽ）
const apiData = ref(null);

// 画面が開いた瞬間に「自動で1回だけ実行される」処理
onMounted(async () => {
  try {
    // 会社ルール：URLは直接書かず、環境変数（.env）から取得する（無ければローカルの8000番を使う設定）
    const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
    
    // バックエンドの「窓口」にデータを注文（リクエスト）する
    const response = await axios.get(`${baseUrl}/api/analysis`);
    
    // 受け取ったデータを入れ物に保存
    apiData.value = response.data;
    
    // デバッグ用：ちゃんと受け取れたか、画面の裏側（コンソール）に出力して確認
    console.log('🔗 バックエンドからデータを受け取りました！', apiData.value);
    
  } catch (error) {
    // もし通信に失敗したらエラーを出す
    console.error('❌ データの取得に失敗しました:', error);
  }
});
</script>