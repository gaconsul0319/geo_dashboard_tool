import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime
import random # 追加：ダミーデータを生成するための標準ライブラリ
from routers import jobs
from routers import export

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Firebaseの初期化設定 ---
try:
    cred = credentials.Certificate("firebase-credentials.json")
    
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'geo-viewer-app.firebasestorage.app'
    })
    
    db = firestore.client()
    logger.info("Firebase Firestore & Storage に正常に接続しました！")
except Exception as e:
    logger.error(f"Firebaseの初期化エラー: {e}")
# ----------------------------

app = FastAPI()
app.include_router(jobs.router)
app.include_router(export.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    logger.info(f"--- アップロード開始: {file.filename} ---")
    
    try:
        # 1. ファイルの読み込みと行数のカウント
        content = await file.read()
        lines = content.decode("utf-8").splitlines()
        id_count = len(lines)
        logger.info(f"ファイルの読み込み成功: {id_count} 件")
        
        # 2. Cloud Storage（倉庫）へ実際のファイルを保存
        bucket = storage.bucket() 
        storage_path = f"csv_uploads/{file.filename}" 
        blob = bucket.blob(storage_path)
        
        blob.upload_from_string(content, content_type='text/csv')
        logger.info(f"Cloud Storageにファイルを保存しました: {storage_path}")

        # 3. Firestore（データベース）に保存するメタデータの作成
        upload_record = {
            "filename": file.filename,
            "id_count": id_count,
            "storage_path": storage_path, 
            "upload_time": datetime.now(), # ★ここでエラーが起きていました
            "status": "completed"
        }
        
        # 4. Firestoreの「uploads」コレクションに記録を保存
        doc_ref = db.collection("uploads").document()
        doc_ref.set(upload_record)
        logger.info(f"Firestoreに記録を保存しました。ドキュメントID: {doc_ref.id}")
        
        return {
            "status": "success",
            "filename": file.filename,
            "count": id_count,
            "message": f"{id_count}件のADIDを受理し、本体をStorageに、記録をデータベースに保存しました。"
        }
    except Exception as e:
        logger.error(f"エラー発生: {str(e)}")
        raise HTTPException(status_code=500, detail="処理に失敗しました。")

@app.get("/api/analysis")
async def get_analysis_data():
    """
    来訪分析画面のグラフ用データを提供するAPI
    ※現在はダミーデータを返していますが、後でBigQueryなどから取得する処理に差し替えます
    """
    logging.info("📊 [開始] グラフ用データ(/api/analysis)の取得リクエストを受け付けました")
    
    try:
        # フロントエンドに渡すデータを準備
        response_data = {
            "status": "success",
            "data": {
                "line_chart": {
                    "labels": ["3/1", "3/2", "3/3", "3/4", "3/5", "3/6", "3/7"],
                    "data": [120, 150, 180, 130, 200, 250, 210]
                },
                "hourly_bar_chart": {
                    "labels": ["10時", "11時", "12時", "13時", "14時"],
                    "data": [15, 30, 55, 42, 20]
                },
                "weekly_bar_chart": {
                    "labels": ["月", "火", "水", "木", "金", "土", "日"],
                    "data": [120, 150, 140, 130, 200, 350, 320]
                }
            }
        }
        
        logging.info("✅ [成功] グラフ用データを返却します")
        return response_data

    except Exception as e:
        logging.error(f"❌ [失敗] グラフ用データの取得中にエラーが発生しました: {e}")
        return {"status": "error", "message": str(e)}
    
# 追加：地図用のデータを返すAPI
@app.get("/api/map-data")
async def get_map_data():
    """
    エリア可視化画面の地図用データを提供するAPI
    ※現在はバックエンドで生成したダミーデータを返していますが、後で実データに差し替えます
    """
    logging.info("[開始] 地図用データ(/api/map-data)の取得リクエストを受け付けました")
    try:
        data = []
        # 東京駅周辺に1000件のデータを生成
        for _ in range(1000):
            data.append({
                "position": [
                    139.7671 + (random.random() - 0.5) * 0.05,
                    35.6812 + (random.random() - 0.5) * 0.05
                ],
                "weight": random.randint(1, 10)
            })
        
        logging.info("[成功] 地図用データを返却します")
        return {"status": "success", "data": data}
    except Exception as e:
        logging.error(f"[失敗] 地図用データの取得中にエラーが発生しました: {e}")
        return {"status": "error", "message": str(e)}

# 新規追加：ダッシュボード用のサマリデータを返すAPI
@app.get("/api/dashboard-summary")
async def get_dashboard_summary():
    """
    ダッシュボード画面の上部に表示するKPIデータを返すAPI
    ※現在は固定のダミー数値を返していますが、後でFirestoreやBigQueryから実際の数値を計算して返すように改修します
    """
    logger.info("[開始] ダッシュボードサマリ(/api/dashboard-summary)の取得リクエストを受け付けました")
    try:
        # フロントエンドに渡すデータ
        summary_data = {
            "total_id": 8530000,
            "completed_tasks": 127,
            "pending_tasks": 3,
            "active_users": 8
        }
        logger.info("[成功] ダッシュボードサマリデータを返却します")
        return summary_data
    except Exception as e:
        logger.error(f"[失敗] ダッシュボードサマリの取得中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="データの取得に失敗しました")

# --- この下のコードを追加 ---
if __name__ == "__main__":
    import uvicorn
    # アプリケーションをポート8000番で起動し、待機状態にする
    uvicorn.run(app, host="127.0.0.1", port=8000)