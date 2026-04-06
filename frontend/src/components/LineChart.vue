<template>
  <div style="height: 200px;">
    <Line :data="formattedData" :options="chartOptions" />
  </div>
</template>

<script setup>
// 【変更後】 computed を追加
import { ref, computed } from 'vue'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

//【変更後】 新規追加：生データを緑色の折れ線グラフ用に変換
const formattedData = computed(() => {
  return {
    labels: props.chartData.labels,
    datasets: [
      {
        label: '来訪UU数',
        borderColor: '#10b981', // 線の色（爽やかな緑色）
        backgroundColor: '#10b981', // 点の色
        data: props.chartData.data,
        tension: 0.4
      }
    ]
  }
});

// グラフの見た目や動きの設定
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false
})

// デバッグ用ログ
console.log('📈 LineChartコンポーネントの準備が完了しました！');
</script>