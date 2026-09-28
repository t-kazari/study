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
        query = select(EmployeeModel)

        # 部署での絞り込み
        if department:
            query = query.where(EmployeeModel.department == department)

        # キーワード検索（氏名、社員番号、メールアドレスの部分一致）
        if keyword:
            search_pattern = f"%{keyword}%"
            query = query.where(
                or_(
                    EmployeeModel.name.like(search_pattern),
                    EmployeeModel.employee_code.like(search_pattern),
                    EmployeeModel.email.like(search_pattern),
                )
            )

        query = query.order_by(EmployeeModel.id.asc())
        return list(db.scalars(query).all())

    def get_by_id(self, db: Session, employee_id: int) -> Optional[EmployeeModel]:
        return db.get(EmployeeModel, employee_id)

    def get_by_code(self, db: Session, employee_code: str) -> Optional[EmployeeModel]:
        query = select(EmployeeModel).where(EmployeeModel.employee_code == employee_code)
        return db.scalars(query).first()

    def get_by_email(self, db: Session, email: str) -> Optional[EmployeeModel]:
        query = select(EmployeeModel).where(EmployeeModel.email == email)
        return db.scalars(query).first()

    def create(self, db: Session, employee: EmployeeCreate) -> EmployeeModel:
        db_employee = EmployeeModel(
            employee_code=employee.employee_code,
            name=employee.name,
            email=employee.email,
            department=employee.department,
            position=employee.position,
            joined_date=employee.joined_date,
            status=employee.status,
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    def update(
        self,
        db: Session,
        employee_id: int,
        employee: EmployeeUpdate,
    ) -> Optional[EmployeeModel]:
        db_employee = self.get_by_id(db, employee_id)
        if not db_employee:
            return None

        update_data = employee.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)

        db.commit()
        db.refresh(db_employee)
        return db_employee

    def delete(self, db: Session, employee_id: int) -> bool:
        db_employee = self.get_by_id(db, employee_id)
        if not db_employee:
            return False

        db.delete(db_employee)
        db.commit()
        return True
