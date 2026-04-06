import streamlit as st
import pandas as pd

st.title("案件管理")
st.write("過去から現在までの全案件のステータス確認・管理を行います。")

# ダミーの案件データを作成
data = {
    "案件名": ["春のキャンペーンA", "新店舗オープン告知", "既存顧客向けセールの分析"],
    "ステータス": ["完了", "処理中", "待機中"],
    "ADID数": [500000, 1200000, 300000],
    "担当者": ["佐藤", "鈴木", "高橋"],
    "処理日時": ["2026-04-01 10:00", "2026-04-05 14:30", "-"]
}

# データを表形式（DataFrame）に変換
df = pd.DataFrame(data)

# 画面に表を表示
st.dataframe(df, use_container_width=True)