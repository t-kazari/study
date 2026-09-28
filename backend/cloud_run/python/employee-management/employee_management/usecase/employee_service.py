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
        """社員一覧を取得する"""
        return self.repository.get_all(db, keyword=keyword, department=department)

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
        """社員を新規登録する（社員番号・メールの重複チェック付き）"""
        # 社員番号の重複チェック
        if self.repository.get_by_code(db, employee_data.employee_code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"社員番号 '{employee_data.employee_code}' は既に登録されています",
            )

        # メールの重複チェック
        if self.repository.get_by_email(db, employee_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"メールアドレス '{employee_data.email}' は既に登録されています",
            )

        return self.repository.create(db, employee_data)

    def update_employee(
        self,
        db: Session,
        employee_id: int,
        employee_data: EmployeeUpdate,
    ) -> EmployeeModel:
        """社員情報を更新する（行内編集対応）"""
        # 存在チェック
        existing = self.repository.get_by_id(db, employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )

        # メールアドレス変更時の重複チェック（他人が既に使っていないか）
        if employee_data.email and employee_data.email != existing.email:
            email_owner = self.repository.get_by_email(db, employee_data.email)
            if email_owner and email_owner.id != employee_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"メールアドレス '{employee_data.email}' は既に使用されています",
                )

        updated = self.repository.update(db, employee_id, employee_data)
        return updated

    def delete_employee(self, db: Session, employee_id: int) -> None:
        """社員を物理削除する"""
        existing = self.repository.get_by_id(db, employee_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"社員ID: {employee_id} が見つかりません",
            )

        self.repository.delete(db, employee_id)
