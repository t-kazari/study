from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from employee_management import config
from employee_management.handler.employee_handler import router as employee_router
from employee_management.infra import employee_impl  # noqa: F401 Table登録用

app = FastAPI(
    title="社員名簿管理 API (Employee Management API)",
    description="新人エンジニアOJT用 社員CRUD操作バックエンドサービス (FastAPI + databases + SQLAlchemy Core)",
    version="1.0.0",
)

# CORS設定（Next.jsフロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """アプリケーション起動時にDB接続プールを確立し、テーブルを作成"""
    try:
        config.metadata.create_all(bind=config.engine)
    except Exception as e:
        print(f"Table creation check warning: {e}")
    await config.database.connect()


@app.on_event("shutdown")
async def shutdown():
    """アプリケーション停止時にDB接続プールを切断"""
    await config.database.disconnect()


@app.get("/health", tags=["health"])
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok", "service": "employee-management-backend"}


# 社員管理ルーターの登録
app.include_router(employee_router)
