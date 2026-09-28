from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeBase(BaseModel):
    """社員基底スキーマ"""
    employee_code: str = Field(..., max_length=20, description="社員番号（例: EMP001）")
    name: str = Field(..., min_length=1, max_length=100, description="氏名")
    email: EmailStr = Field(..., description="メールアドレス")
    department: str = Field(..., max_length=50, description="所属部署")
    position: str = Field(..., max_length=50, description="役職")
    joined_date: date = Field(..., description="入社日（YYYY-MM-DD）")
    status: str = Field(default="在籍", max_length=20, description="在籍ステータス")


class EmployeeCreate(EmployeeBase):
    """社員新規作成リクエストスキーマ"""
    pass


class EmployeeUpdate(BaseModel):
    """社員情報更新リクエストスキーマ（行内編集用）"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="氏名")
    email: Optional[EmailStr] = Field(None, description="メールアドレス")
    department: Optional[str] = Field(None, max_length=50, description="所属部署")
    position: Optional[str] = Field(None, max_length=50, description="役職")
    joined_date: Optional[date] = Field(None, description="入社日（YYYY-MM-DD）")
    status: Optional[str] = Field(None, max_length=20, description="在籍ステータス")


class EmployeeResponse(EmployeeBase):
    """社員情報レスポンススキーマ"""
    id: int = Field(..., description="社員ID")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    model_config = ConfigDict(from_attributes=True)
