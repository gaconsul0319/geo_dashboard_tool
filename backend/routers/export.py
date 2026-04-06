import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

# このファイル専用の受付窓口を作ります
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/api/export/csv")
async def export_csv():
    """
    分析データをCSV形式でダウンロードするAPI
    ※今回はテスト用にダミーのCSVデータを返します。
    """
    logger.info("📥 [開始] CSVダウンロード(/api/export/csv)のリクエストを受け付けました")
    try:
        # カンマ区切りの文字列（CSVの元データ）を作成します
        csv_content = "日付,来訪UU数,総来訪回数\n2026-04-01,120,150\n2026-04-02,150,180\n2026-04-03,180,210\n"
        
        logger.info("✅ [成功] CSVデータを返却します")
        
        # ただの文字ではなく「ダウンロード用のCSVファイル」として渡すための設定です
        return Response(
            content=csv_content.encode("utf-8-sig"), # 文字化けを防ぐおまじない
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=analysis_data.csv"}
        )
        
    except Exception as e:
        logger.error(f"❌ [失敗] CSVの作成中にエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="ファイルの作成に失敗しました")