from typing import List, Optional
from fastapi import HTTPException, status
from injector import inject
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate
from employee_management.repository.employee_repository import EmployeeRepository


class EmployeeService:
    """社員管理ビジネスロジック（Usecase層）"""

    @inject
    def __init__(self, repository: EmployeeRepository):
        # 抽象インターフェース EmployeeRepository をインジェクション
        self.repository = repository

    async def get_employees(
        self,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[dict]:
        """社員一覧を取得する"""
        return await self.repository.get_all(keyword=keyword, department=department)

    async def get_employee_by_id(self, employee_id: int) -> dict:
        """指定IDの社員を取得する"""
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )
        return employee

    async def create_employee(self, employee_data: EmployeeCreate) -> dict:
        """社員を新規登録する（社員番号・メールの重複チェック付き）"""
        # 社員番号の重複チェック
        if await self.repository.get_by_code(employee_data.employee_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"社員番号 '{employee_data.employee_code}' は既に登録されています",
            )

        # メールの重複チェック
        if await self.repository.get_by_email(employee_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"メールアドレス '{employee_data.email}' は既に登録されています",
            )

        return await self.repository.create(employee_data)

    async def update_employee(
        self,
        employee_id: int,
        employee_data: EmployeeUpdate,
    ) -> dict:
        """社員情報を更新する（行内編集対応）"""
        # 存在チェック
        existing = await self.repository.get_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )

        # メールアドレス変更時の重複チェック（他人が既に使用していないか）
        if employee_data.email and employee_data.email != existing["email"]:
            email_owner = await self.repository.get_by_email(employee_data.email)
            if email_owner and email_owner["id"] != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"メールアドレス '{employee_data.email}' は既に使用されています",
                )

        updated = await self.repository.update(employee_id, employee_data)
        return updated

    async def delete_employee(self, employee_id: int) -> None:
        """社員を物理削除する"""
        existing = await self.repository.get_by_id(employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )

        await self.repository.delete(employee_id)
