"""スケジュール管理システムのメインFastAPIアプリケーション。

このモジュールはスケジュール管理用のFastAPIアプリケーションのエントリポイントです。
"""

from fastapi import FastAPI
from typing import List
from interfaces import ScheduleCreate, ScheduleUpdate, ScheduleResponse
import api

app = FastAPI(title="Schedule Management API", version="1.0.0")


@app.get("/")
def read_root():
    """ウェルカムメッセージを返すルートエンドポイント。
    
    戻り値:
        ウェルカムメッセージを含む辞書。
    """
    return {"message": "Schedule Management API"}


@app.post("/schedules/", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate):
    return api.create_schedule(schedule)


@app.get("/schedules/", response_model=List[ScheduleResponse])
def read_schedules(skip: int = 0, limit: int = 100):
    return api.read_schedules(skip, limit)


@app.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
def read_schedule(schedule_id: int):
    return api.read_schedule(schedule_id)


@app.put("/schedules/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(schedule_id: int, schedule_update: ScheduleUpdate):
    return api.update_schedule(schedule_id, schedule_update)


@app.delete("/schedules/{schedule_id}")
def delete_schedule(schedule_id: int):
    return api.delete_schedule(schedule_id)


if __name__ == "__main__":
    """uvicornサーバーでFastAPIアプリケーションを実行します。
    
    このブロックはスクリプトが直接実行されたときに実行されます。
    すべてのインターフェース (0.0.0.0) のポート 8000 でuvicornサーバーを起動します。
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)