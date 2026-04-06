<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <h1 class="text-2xl font-bold text-gray-800">ダッシュボード</h1>
      <span class="text-sm text-gray-500 font-medium">システム稼働状況・KPIサマリ</span>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm font-medium text-gray-500 mb-1">当月処理ADID数</p>
        <p class="text-2xl font-bold text-gray-800">{{ summary.total_id.toLocaleString() }}</p>
        <p class="text-xs text-gray-400 mt-2">上限: 25,000,000</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm font-medium text-gray-500 mb-1">完了案件</p>
        <p class="text-2xl font-bold text-blue-600">{{ summary.completed_tasks }}</p>
        <p class="text-xs text-gray-400 mt-2">月間目標 200</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm font-medium text-gray-500 mb-1">処理中 / 待機中</p>
        <p class="text-2xl font-bold text-orange-500">{{ summary.pending_tasks }} / 5</p>
        <p class="text-xs text-gray-400 mt-2">キュー内 8案件</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm font-medium text-gray-500 mb-1">アクティブユーザー</p>
        <p class="text-2xl font-bold text-emerald-600">{{ summary.active_users }}</p>
        <p class="text-xs text-gray-400 mt-2">15名中</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
          <h2 class="text-sm font-bold text-gray-800">バッチ処理キュー（リアルタイム）</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-white text-xs text-gray-500 border-b border-gray-100">
                <th class="px-6 py-3 font-medium">案件名</th>
                <th class="px-6 py-3 font-medium">ステータス</th>
                <th class="px-6 py-3 font-medium">ADID数</th>
                <th class="px-6 py-3 font-medium">進捗</th>
              </tr>
            </thead>
            <tbody class="text-sm text-gray-700 divide-y divide-gray-100">
              <tr class="hover:bg-gray-50 transition">
                <td class="px-6 py-4 font-medium">春CP_東京</td>
                <td class="px-6 py-4"><span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">処理中</span></td>
                <td class="px-6 py-4">520,000</td>
                <td class="px-6 py-4 text-gray-500">残り 2分</td>
              </tr>
              <tr class="hover:bg-gray-50 transition">
                <td class="px-6 py-4 font-medium">GW施策_大阪</td>
                <td class="px-6 py-4"><span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">処理中</span></td>
                <td class="px-6 py-4">310,000</td>
                <td class="px-6 py-4 text-gray-500">残り 5分</td>
              </tr>
              <tr class="hover:bg-gray-50 transition">
                <td class="px-6 py-4 font-medium">新商品LP_全国</td>
                <td class="px-6 py-4"><span class="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs font-bold">待機中</span></td>
                <td class="px-6 py-4">980,000</td>
                <td class="px-6 py-4 text-gray-500">キュー #1</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-between">
        <div>
          <h2 class="text-sm font-bold text-gray-800 mb-6">コスト消化率</h2>
          <div class="flex items-end justify-between mb-2">
            <span class="text-3xl font-bold text-gray-800">{{ ((summary.total_id / 25000000) * 100).toFixed(1) }}%</span>
            <span class="text-sm text-gray-500 mb-1">{{ (summary.total_id / 1000000).toFixed(1) }}M / 25M ID</span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-3 mb-4 overflow-hidden">
            <div class="bg-blue-500 h-3 rounded-full" :style="{ width: ((summary.total_id / 25000000) * 100) + '%' }"></div>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed">
            当月予算上限の80%に到達するとソフトリミット警告が表示されます。
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// フェーズ3で作った大切なAPI通信の道具を再利用
import api from '../api';

// 取得したデータを保存する変数（初期値は0）
const summary = ref({
  total_id: 0,
  completed_tasks: 0,
  pending_tasks: 0,
  active_users: 0
});

// 画面が表示された時にバックエンドのAPIを呼び出す
onMounted(async () => {
  console.log('[Dashboard] ダッシュボード画面がマウントされました。APIからデータを取得します...');
  try {
    const response = await api.get('/api/dashboard-summary');
    summary.value = response.data;
    console.log('[Dashboard] API通信成功！データを画面に反映しました。', response.data);
  } catch (error) {
    console.error('[Dashboard] API通信エラー:', error);
  }
});
</script>