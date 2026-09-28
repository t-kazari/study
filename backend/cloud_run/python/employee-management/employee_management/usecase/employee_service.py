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
        # TODO: [課題1] リポジトリの一覧取得メソッドを非同期呼び出ししてください
        # return await self.repository.get_all(keyword=keyword, department=department)
        pass

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
        # TODO: [課題2] 社員新規登録の業務ルール（重複チェック）を実装してください
        # 1. await self.repository.get_by_code() で社員番号の重複をチェック（重複時は HTTPException 400）
        # 2. await self.repository.get_by_email() でメールアドレスの重複をチェック（重複時は HTTPException 400）
        # 3. await self.repository.create() を呼び出して作成結果を返してください
        pass

    async def update_employee(
        self,
        employee_id: int,
        employee_data: EmployeeUpdate,
    ) -> dict:
        # TODO: [課題3] 社員情報更新の業務ルールを実装してください
        # 1. 存在チェック（await self.repository.get_by_id で見つからなければ 404）
        # 2. メールアドレス変更時の重複チェック（他人が既に使用していないかチェック）
        # 3. await self.repository.update() を呼び出して更新結果を返してください
        pass

    async def delete_employee(self, employee_id: int) -> None:
        # TODO: [課題4] 社員削除の業務ルールを実装してください
        # 1. 存在チェック（見つからなければ 404）
        # 2. await self.repository.delete() を呼び出して削除してください
        pass
