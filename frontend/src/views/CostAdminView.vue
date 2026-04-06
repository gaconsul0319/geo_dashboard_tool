<template>
  <div class="space-y-6">
    <div class="flex items-end justify-between border-b pb-4">
      <div class="flex items-center space-x-4">
        <h1 class="text-2xl font-bold text-gray-800">コスト管理</h1>
        <span class="px-2 py-1 bg-red-100 text-red-700 text-[10px] font-bold rounded italic">管理者権限</span>
      </div>
      <div class="text-sm text-gray-500 font-medium">当月利用状況・アラート設定</div>
    </div>

    <div class="grid grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm text-gray-500 font-medium mb-4">当月ADID処理数</p>
        <div class="flex justify-between items-end mb-2">
          <p class="text-3xl font-bold text-gray-800">8,530,000 <span class="text-sm text-gray-400 font-normal">/ 25,000,000 ID</span></p>
          <p class="text-sm font-bold text-blue-600">34.1%</p>
        </div>
        <div class="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
          <div class="bg-blue-500 h-full transition-all duration-500" style="width: 34.1%"></div>
        </div>
      </div>
      
      <div class="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <p class="text-sm text-gray-500 font-medium mb-4">当月発生費用（概算）</p>
        <div class="flex items-baseline space-x-2">
          <p class="text-3xl font-bold text-gray-800">¥ 2,480,000</p>
          <span class="text-xs text-gray-400">※従量課金＋基本料金</span>
        </div>
        <p class="text-xs text-green-500 font-bold mt-4 italic">予算内：正常稼働中</p>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-6">
      <div class="col-span-1 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-sm font-bold text-gray-800 mb-6 flex items-center">
          <span class="mr-2">🔔</span>ソフト＆ハードリミット設定
        </h2>
        <div class="space-y-6">
          <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-100">
            <div>
              <p class="text-xs font-bold text-yellow-800">ソフトリミット① (80%)</p>
              <p class="text-[10px] text-yellow-600">管理者警告メール送信</p>
            </div>
            <input type="checkbox" checked class="w-4 h-4 text-yellow-600">
          </div>
          <div class="flex items-center justify-between p-3 bg-orange-50 rounded-lg border border-orange-100">
            <div>
              <p class="text-xs font-bold text-orange-800">ソフトリミット② (90%)</p>
              <p class="text-[10px] text-orange-600">再通知 ＆ 注意喚起表示</p>
            </div>
            <input type="checkbox" checked class="w-4 h-4 text-orange-600">
          </div>
          <div class="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-100">
            <div>
              <p class="text-xs font-bold text-red-800">ハードリミット (100%)</p>
              <p class="text-[10px] text-red-600">全員の送信ボタン強制無効化</p>
            </div>
            <input type="checkbox" checked class="w-4 h-4 text-red-600">
          </div>
          <button class="w-full py-2 bg-gray-800 text-white text-xs font-bold rounded-lg hover:bg-black transition">
            設定を更新する
          </button>
        </div>
      </div>

      <div class="col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h2 class="text-sm font-bold text-gray-800 mb-4 flex items-center">
          <span class="mr-2">👤</span>ユーザー別利用状況（当月）
        </h2>
        <div class="space-y-4">
          <div v-for="(user, index) in ['田中太郎', '鈴木花子', '佐藤健一', '山田美咲']" :key="index" class="space-y-1">
            <div class="flex justify-between text-xs font-medium text-gray-600">
              <span>{{ user }}</span>
              <span>{{ (2.2 - index * 0.3).toFixed(1) }}M ID</span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
              <div class="bg-gray-400 h-full" :style="{ width: (40 - index * 8) + '%' }"></div>
            </div>
          </div>
          <p class="text-right text-[10px] text-gray-400 mt-4 underline cursor-pointer">全ユーザーの履歴を表示</p>
        </div>
      </div>
    </div>

  </div>
</template>