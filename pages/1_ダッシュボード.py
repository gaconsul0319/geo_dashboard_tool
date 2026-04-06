import streamlit as st
import pandas as pd

st.set_page_config(page_title="ダッシュボード", layout="wide")

# --- カスタムCSS（徹底的な余白削減とサイドバー白文字化） ---
st.markdown("""
<style>
/* ① 画面全体の上下余白を極限まで減らす */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
}
/* ② サイドバーのメニュー文字を強制的に白にする */
[data-testid="stSidebarNav"] span {
    color: white !important;
}
/* ③ メトリクス（数字）のカード化と余白削減 */
div[data-testid="metric-container"] {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 10px !important; 
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
/* ④ 見出し周りの余白を削る */
h3 {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}
/* ⑤ アラート（警告枠）の余白を削る */
div[data-testid="stAlert"] {
    padding: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)
# ----------------------------------

# タイトルもコンパクトにするため markdown を使用
st.markdown("### ダッシュボード <span style='font-size:14px; font-weight:normal; color:gray;'>処理状況・KPIサマリ一覧</span>", unsafe_allow_html=True)

# アラート表示
st.warning("コストアラート：当月利用ID数が上限の 41.5% に到達しました（1,245,320 / 3,000,000）", icon="⚠️")

# 1. 上部：KPIを4つ横並び
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="当月処理ADID数", value="1,245,320")
with col2:
    st.metric(label="完了案件数", value="42")
with col3:
    st.metric(label="処理中案件", value="3")
with col4:
    st.metric(label="アクティブユーザー", value="5")

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True) # 最小限のすき間

# 2. 中部：グラフとリストを配置
chart_col, list_col = st.columns([2, 1.2]) 

with chart_col:
    with st.container(border=True):
        st.markdown("##### 月間処理ADID推移")
        chart_data = pd.DataFrame(
            {"ADID数": [980000, 1120000, 1350000, 1050000, 1245320, 890000]},
            index=["1月", "2月", "3月", "4月", "5月", "6月"]
        )
        # height=230 を指定してグラフの高さを抑える！
        st.bar_chart(chart_data, color="#0083b0", height=230)

with list_col:
    with st.container(border=True):
        st.markdown("##### 最近の処理状況")
        # 箱（アラート）を使うと余白が大きすぎるため、HTMLでコンパクトなリストを作成
        st.markdown("""
        <div style="font-size: 14px; line-height: 2.0;">
            ✅ <b>完了</b>：春キャンペーン_東京 <span style="color:gray;">(2分前)</span><br>
            ⏳ <span style="color:#cc8800;"><b>処理中</b></span>：GW施策_大阪エリア <span style="color:gray;">(5分前)</span><br>
            ✅ <b>完了</b>：新商品LP_全国 <span style="color:gray;">(15分前)</span><br>
            ⏸ <span style="color:#cc0000;"><b>待機</b></span>：梅雨セール_九州 <span style="color:gray;">(20分前)</span><br>
            ✅ <b>完了</b>：リタゲ施策_関東 <span style="color:gray;">(1時間前)</span>
        </div>
        """, unsafe_allow_html=True)