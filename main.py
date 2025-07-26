"""スケジュール管理システムのメインFastAPIアプリケーション。

このモジュールはスケジュール管理用のFastAPIアプリケーションと
APIエンドポイントを含んでいます。アプリケーションのエントリポイントとして機能します。
"""

from fastapi import FastAPI, HTTPException
from typing import List
from interfaces import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from implementations import create_schedule_service

app = FastAPI(title="Schedule Management API", version="1.0.0")

schedule_service = create_schedule_service()


@app.get("/")
def read_root():
    """ウェルカムメッセージを返すルートエンドポイント。
    
    戻り値:
        ウェルカムメッセージを含む辞書。
    """
    return {"message": "Schedule Management API"}


@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate):
    """新しいスケジュールを作成します。
    
    引数:
        schedule: 作成するスケジュールデータ。
        
    戻り値:
        作成されたスケジュールレスポンス。
    """
    return schedule_service.create_schedule(schedule)


@app.get("/schedules/", response_model=List[ScheduleResponse])
def read_schedules(skip: int = 0, limit: int = 100):
    """ページネーション付きですべてのスケジュールを取得します。
    
    引数:
        skip: ページネーション用にスキップするスケジュール数。
        limit: 返すスケジュールの最大数。
        
    戻り値:
        スケジュールレスポンスのリスト。
    """
    return schedule_service.get_schedules(skip, limit)


@app.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
def read_schedule(schedule_id: int):
    """IDによって特定のスケジュールを取得します。
    
    引数:
        schedule_id: 取得するスケジュールのID。
        
    戻り値:
        スケジュールレスポンス。
        
    例外:
        HTTPException: スケジュールが見つからない場合 (404)。
    """
    schedule = schedule_service.get_schedule(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@app.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate):
    """既存のスケジュールを更新します。
    
    引数:
        schedule_id: 更新するスケジュールのID。
        schedule_update: 更新データ。
        
    戻り値:
        更新されたスケジュールレスポンス。
        
    例外:
        HTTPException: スケジュールが見つからない場合 (404)。
    """
    schedule = schedule_service.update_schedule(schedule_id, schedule_update)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int):
    """IDによってスケジュールを削除します。
    
    引数:
        schedule_id: 削除するスケジュールのID。
        
    戻り値:
        成功メッセージ。
        
    例外:
        HTTPException: スケジュールが見つからない場合 (404)。
    """
    success = schedule_service.delete_schedule(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "Schedule deleted successfully"}


if __name__ == "__main__":
    """uvicornサーバーでFastAPIアプリケーションを実行します。
    
    このブロックはスクリプトが直接実行されたときに実行されます。
    すべてのインターフェース (0.0.0.0) のポート 8000 でuvicornサーバーを起動します。
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)