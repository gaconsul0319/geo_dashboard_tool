import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../firebase'
import { onAuthStateChanged } from 'firebase/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
    { path: '/dashboard', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
    { path: '/campaigns', name: 'campaigns', component: () => import('../views/CampaignsView.vue') },
    { path: '/upload', name: 'upload', component: () => import('../views/UploadView.vue') },
    { path: '/area-viz', name: 'area-viz', component: () => import('../views/AreaVizView.vue') },
    { path: '/analysis', name: 'analysis', component: () => import('../views/VisitAnalysisView.vue') },
    { path: '/cost', name: 'cost', component: () => import('../views/CostAdminView.vue') },
    { path: '/export', name: 'export', component: () => import('../views/ExportView.vue') }
  ]
})

// Firebaseのログイン状態を正確に待つための関数
const getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = onAuthStateChanged(auth, user => {
      unsubscribe()
      resolve(user)
    }, reject)
  })
}

// 画面が切り替わる「前」に毎回必ず実行される見張り番（ルートガード）
router.beforeEach(async (to, from, next) => {
  const isLoginRoute = to.path === '/login'
  const user = await getCurrentUser()

  if (!isLoginRoute && !user) {
    // ログイン画面以外を見ようとしているのに、ログインしていない場合 → ログイン画面へ強制送還
    next('/login')
  } else if (isLoginRoute && user) {
    // ログイン画面を見ようとしているのに、すでにログイン済みの場合 → ダッシュボードへ飛ばす
    next('/dashboard')
  } else {
    // 問題ない場合はそのまま画面を表示
    next()
  }
})

export default router