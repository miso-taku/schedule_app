from fastapi import FastAPI
from presentation.routes.schedule_routes import router as schedule_router

app = FastAPI(title="Schedule Management API", version="1.0.0")

app.include_router(schedule_router)


@app.get("/")
def read_root():
    return {"message": "Schedule Management API"}


if __name__ == "__main__":
    """uvicornサーバーでFastAPIアプリケーションを実行します。
    
    このブロックはスクリプトが直接実行されたときに実行されます。
    すべてのインターフェース (0.0.0.0) のポート 8000 でuvicornサーバーを起動します。
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)