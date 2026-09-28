from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from employee_management.config import Base, engine
from employee_management.handler.employee_handler import router as employee_router
from employee_management.infra.employee_impl import EmployeeModel  # noqa: F401

# DBテーブルが存在しない場合は自動作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="社員名簿管理 API (Employee Management API)",
    description="新人エンジニアOJT用 社員CRUD操作バックエンドサービス",
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


@app.get("/health", tags=["health"])
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "ok", "service": "employee-management-backend"}


# 社員管理ルーターの登録
app.include_router(employee_router)
