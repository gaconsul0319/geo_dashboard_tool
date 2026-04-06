<script setup>
import { ref, onMounted } from 'vue'
import { RouterView, useRouter, RouterLink } from 'vue-router'
import { auth } from './firebase'
import { signOut, onAuthStateChanged } from 'firebase/auth'

const router = useRouter()
const isAuthenticated = ref(false)

// ログイン状態を常に監視して、メニューの表示/非表示を切り替える
onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    isAuthenticated.value = !!user
  })
})

// ログアウト処理
const handleLogout = async () => {
  try {
    await signOut(auth)
    // ログアウト成功後、ログイン画面へ強制送還
    router.push('/login')
  } catch (error) {
    console.error('ログアウトエラー:', error)
    alert('ログアウトに失敗しました。')
  }
}
</script>

<template>
  <div class="flex h-screen bg-slate-50">
    
    <nav v-if="isAuthenticated" class="w-48 md:w-56 bg-[#161b22] text-white flex flex-col shadow-xl z-10">
      <div class="p-6 border-b border-gray-700/50">
        <h1 class="text-xl font-bold tracking-wider text-center">GEO Viewer</h1>
      </div>
      
      <div class="flex-1 overflow-y-auto py-6">
        <ul class="space-y-1">
          <li><RouterLink to="/dashboard" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">ダッシュボード</RouterLink></li>
          <li><RouterLink to="/campaigns" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">案件管理</RouterLink></li>
          <li><RouterLink to="/upload" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">CSVアップロード</RouterLink></li>
          <li><RouterLink to="/area-viz" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">エリア可視化</RouterLink></li>
          <li><RouterLink to="/analysis" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">来訪分析</RouterLink></li>
          <li><RouterLink to="/cost" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">コスト管理</RouterLink></li>
          <li><RouterLink to="/export" class="block px-6 py-3 text-sm hover:bg-blue-600 transition-colors" active-class="bg-blue-600 font-bold">エクスポート</RouterLink></li>
        </ul>
      </div>

      <div class="p-4 border-t border-gray-700/50">
        <button @click="handleLogout" class="w-full py-2.5 px-4 bg-gray-800 hover:bg-red-500 hover:text-white text-gray-300 text-sm font-bold rounded-lg transition-colors flex items-center justify-center">
          <span>ログアウト</span>
        </button>
      </div>
    </nav>

    <main class="flex-1 overflow-y-auto p-8 relative">
      <RouterView />
    </main>
    
  </div>
</template>

<style>
/* リンクのデフォルトスタイルをリセット */
a {
  text-decoration: none;
}
</style>