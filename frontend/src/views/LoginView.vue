<script setup>
import { auth } from '../firebase';
import { GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth'; // signOutを追加
import { useRouter } from 'vue-router';

const router = useRouter();

const loginWithGoogle = async () => {
  try {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    const userEmail = result.user.email;

    // --- ドメイン制限ロジック ---
    // 1. @gendai-a.co.jp で終わるか
    // 2. または、現在の開発用アカウントであるか
    if (userEmail.endsWith('@gendai-a.co.jp') || userEmail === 'ga.digitalconsul@gmail.com') {
      console.log('ログイン成功:', userEmail);
      router.push('/dashboard');
    } else {
      // 許可されていないドメインの場合は、即座にログアウトさせてエラーを出す
      await signOut(auth);
      alert('このツールは @gendai-a.co.jp のアカウント専用です。\nログインしたアカウント（' + userEmail + '）では利用できません。');
    }
    // ----------------------------

  } catch (error) {
    console.error('ログインエラー:', error);
    alert('ログイン処理中にエラーが発生しました。');
  }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-100">
    <div class="max-w-md w-full bg-white p-10 rounded-2xl shadow-lg border border-gray-100 text-center">
      <div class="text-6xl mb-6">🌍</div>
      <h2 class="text-3xl font-bold text-gray-800 mb-2">GEO Viewer</h2>
      <p class="text-sm text-gray-500 mb-10">社内Googleアカウントでログインしてください</p>
      
      <button @click="loginWithGoogle" class="w-full flex items-center justify-center space-x-3 bg-white border-2 border-gray-200 text-gray-700 px-4 py-3 rounded-xl hover:bg-gray-50 hover:border-blue-300 transition shadow-sm font-bold text-lg">
        <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" class="w-6 h-6" />
        <span>Googleでログイン</span>
      </button>

      <div class="mt-8 pt-6 border-t border-gray-100">
        <p class="text-xs text-red-500 font-medium">※ @gendai-a.co.jp ドメインのアカウントのみ利用可能です。</p>
      </div>
    </div>
  </div>
</template>