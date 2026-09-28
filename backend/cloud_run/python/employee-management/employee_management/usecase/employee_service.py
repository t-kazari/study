from typing import List, Optional
from fastapi import HTTPException, status
from injector import inject
from sqlalchemy.orm import Session
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate
from employee_management.infra.employee_impl import EmployeeModel
from employee_management.repository.employee_repository import EmployeeRepository


class EmployeeService:
    """社員管理ビジネスロジック（Usecase層）"""

    @inject
    def __init__(self, repository: EmployeeRepository):
        # 抽象インターフェース EmployeeRepository をインジェクション
        self.repository = repository

    def get_employees(
        self,
        db: Session,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[EmployeeModel]:
        # TODO: [課題1] リポジトリの一覧取得メソッドを呼び出してください
        # return self.repository.get_all(db, keyword=keyword, department=department)
        pass

    def get_employee_by_id(self, db: Session, employee_id: int) -> EmployeeModel:
        """指定IDの社員を取得する"""
        employee = self.repository.get_by_id(db, employee_id)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )
        return employee

    def create_employee(self, db: Session, employee_data: EmployeeCreate) -> EmployeeModel:
        # TODO: [課題2] 社員新規登録の業務ルール（重複チェック）を実装してください
        # 1. self.repository.get_by_code() で社員番号の重複をチェック（重複時は HTTPException 400）
        # 2. self.repository.get_by_email() でメールアドレスの重複をチェック（重複時は HTTPException 400）
        # 3. self.repository.create() を呼び出して作成結果を返してください
        pass

    def update_employee(
        self,
        db: Session,
        employee_id: int,
        employee_data: EmployeeUpdate,
    ) -> EmployeeModel:
        # TODO: [課題3] 社員情報更新の業務ルールを実装してください
        # 1. 存在チェック（self.repository.get_by_id で見つからなければ 404）
        # 2. メールアドレス変更時の重複チェック（他人が既に使用していないかチェック）
        # 3. self.repository.update() を呼び出して更新結果を返してください
        pass

    def delete_employee(self, db: Session, employee_id: int) -> None:
        # TODO: [課題4] 社員削除の業務ルールを実装してください
        # 1. 存在チェック（見つからなければ 404）
        # 2. self.repository.delete() を呼び出して削除してください
        pass
