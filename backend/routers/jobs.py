import logging
from fastapi import APIRouter, HTTPException
from firebase_admin import firestore

# ルーターの設定（このファイル専用の受付窓口を作ります）
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/api/jobs")
async def get_jobs():
    """
    案件管理画面（キャンペーン一覧）のデータを取得するAPI
    Firestoreから過去にアップロードしたデータを取得して返します。
    """
    logger.info("📋 [開始] 案件一覧(/api/jobs)の取得リクエストを受け付けました")
    try:
        # Firestoreのデータベースに接続
        db = firestore.client()
        
        # 「uploads」コレクションのデータを取得
        # （新しいものが上に来るように、アップロード時間で並び替えます）
        docs = db.collection("uploads").order_by("upload_time", direction=firestore.Query.DESCENDING).stream()
        
        jobs_list = []
        for doc in docs:
            data = doc.to_dict()
            
            # 日時データがある場合は、フロントエンドで扱いやすい文字列に変換
            upload_time = data.get("upload_time")
            if upload_time:
                upload_time = upload_time.isoformat()
            
            # フロントエンドに返すデータを整理してリストに追加
            jobs_list.append({
                "id": doc.id,
                "filename": data.get("filename", "名称未設定"),
                "id_count": data.get("id_count", 0),
                "status": data.get("status", "unknown"),
                "upload_time": upload_time
            })
        
        logger.info(f"✅ [成功] {len(jobs_list)}件の案件データを返却します")
        return {"status": "success", "data": jobs_list}
        
    except Exception as e:
        logger.error(f"❌ [失敗] 案件一覧の取得中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="データの取得に失敗しました")
    
@router.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """
    指定された案件を削除するAPI
    フロントエンドから送られてきた job_id を元に、Firestoreのデータを削除します。
    """
    logger.info(f"🗑️ [開始] 案件削除リクエストを受け付けました。対象ID: {job_id}")
    try:
        db = firestore.client()
        
        # Firestoreの「uploads」コレクションから、指定されたIDのデータを削除
        db.collection("uploads").document(job_id).delete()
        
        logger.info(f"✅ [成功] 案件を削除しました: {job_id}")
        return {"status": "success", "message": "削除が完了しました"}
        
    except Exception as e:
        logger.error(f"❌ [失敗] 案件の削除中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="削除に失敗しました")