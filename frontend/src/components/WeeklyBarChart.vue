<template>
  <div style="height: 200px;">
    <Bar :data="formattedData" :options="chartOptions" />
  </div>
</template>

<script setup>
// ✨【変更後】 computed を追加しました
import { ref, computed } from 'vue'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

// ✨【変更後】 新規追加：生データを紫色の棒グラフ用に変換します
const formattedData = computed(() => {
  return {
    labels: props.chartData.labels,
    datasets: [
      {
        label: '来訪UU数',
        backgroundColor: '#8b5cf6', // グラフの色（紫色）
        data: props.chartData.data
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
console.log('📊 WeeklyBarChartコンポーネントの準備が完了しました！');
</script>