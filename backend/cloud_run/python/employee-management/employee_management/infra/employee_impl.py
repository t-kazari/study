from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Date, DateTime, Integer, String, or_, select
from sqlalchemy.orm import Session
from employee_management.config import Base
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate
from employee_management.repository.employee_repository import EmployeeRepository


class EmployeeModel(Base):
    """SQLAlchemy 社員テーブルORMモデル"""
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    employee_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    department = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    joined_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default="在籍")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class EmployeeRepositoryImpl(EmployeeRepository):
    """EmployeeRepository の MySQL/SQLAlchemy による具象実装クラス"""

    def get_all(
        self,
        db: Session,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[EmployeeModel]:
        # TODO: [課題1] 社員一覧取得処理を実装してください
        # 1. select(EmployeeModel) でクエリを作成します。
        # 2. department が指定されている場合は where(EmployeeModel.department == department) で絞り込みます。
        # 3. keyword が指定されている場合は or_() を使い、name, employee_code, email の部分一致（.like()）で絞り込みます。
        # 4. id 昇順（.order_by(EmployeeModel.id.asc())）で並び替え、list(db.scalars(query).all()) を返してください。
        pass

    def get_by_id(self, db: Session, employee_id: int) -> Optional[EmployeeModel]:
        return db.get(EmployeeModel, employee_id)

    def get_by_code(self, db: Session, employee_code: str) -> Optional[EmployeeModel]:
        # TODO: [課題2] 社員番号での重複チェック用取得クエリを実装してください
        # select(EmployeeModel).where(EmployeeModel.employee_code == employee_code)
        pass

    def get_by_email(self, db: Session, email: str) -> Optional[EmployeeModel]:
        # TODO: [課題2] メールアドレスでの重複チェック用取得クエリを実装してください
        # select(EmployeeModel).where(EmployeeModel.email == email)
        pass

    def create(self, db: Session, employee: EmployeeCreate) -> EmployeeModel:
        # TODO: [課題2] 社員新規登録処理を実装してください
        # 1. EmployeeModel インスタンスを作成します。
        # 2. db.add(db_employee) でセッションに追加します。
        # 3. db.commit() でコミットし、db.refresh(db_employee) で確定データを読み込んで返してください。
        pass

    def update(
        self,
        db: Session,
        employee_id: int,
        employee: EmployeeUpdate,
    ) -> Optional[EmployeeModel]:
        # TODO: [課題3] 社員情報更新処理を実装してください
        # 1. self.get_by_id(db, employee_id) で対象レコードを取得します。存在しなければ None を返します。
        # 2. employee.model_dump(exclude_unset=True) で渡された項目のみ setattr で更新します。
        # 3. db.commit() と db.refresh(db_employee) を実行して返してください。
        pass

    def delete(self, db: Session, employee_id: int) -> bool:
        # TODO: [課題4] 社員の物理削除処理を実装してください
        # 1. self.get_by_id(db, employee_id) で対象レコードを取得します。存在しなければ False を返します。
        # 2. db.delete(db_employee) を実行し、db.commit() を行って True を返してください。
        pass
