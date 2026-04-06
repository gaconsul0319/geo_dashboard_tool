<template>
  <div style="height: 300px;">
    <Bar :data="formattedData" :options="chartOptions" />
  </div>
</template>

<script setup>
// 変更：computed（自動変換機能）を追加でインポート
import { ref, computed } from 'vue'
// Chart.jsから必要な「描画の道具」をインポート（読み込み）
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Bar } from 'vue-chartjs'

// Chart.jsに「これらの道具を使います」と登録
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

// 親画面からデータを受け取るための「窓口（Props）」を作成
// 変更：受け取ったデータを「props」という名前の箱に入れます
const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

// ✨ 新規追加：受け取った生データを、グラフ用の形（色などの設定付き）に自動変換する ✨
const formattedData = computed(() => {
  return {
    labels: props.chartData.labels, // バックエンドから来た「時刻」のデータ
    datasets: [
      {
        label: '来訪者数',
        backgroundColor: '#0ea5e9', // グラフの色（爽やかなブルー）
        data: props.chartData.data  // バックエンドから来た「人数」のデータ
      }
    ]
  }
});

// グラフの見た目や動きの設定
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false
})

// デバッグ用：画面の裏側（コンソール）に成功メッセージを出す
console.log('📊 BarChartコンポーネントの準備が完了しました！');
</script>