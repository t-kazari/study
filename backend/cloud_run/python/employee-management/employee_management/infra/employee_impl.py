from datetime import datetime
from typing import List, Optional
import sqlalchemy
from injector import inject
from employee_management.config import metadata
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate
from employee_management.repository.employee_repository import EmployeeRepository
from employee_management.utils.contextutils import Context

# SQLAlchemy Core Table 定義
employees_table = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("employee_code", sqlalchemy.String(20), unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(150), unique=True, nullable=False),
    sqlalchemy.Column("department", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("position", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("joined_date", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("status", sqlalchemy.String(20), nullable=False, default="在籍"),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, default=datetime.utcnow),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, nullable=False, default=datetime.utcnow),
)


class EmployeeRepositoryImpl(EmployeeRepository):
    """EmployeeRepository の SQLAlchemy Core + Context(databases) による非同期具象実装"""

    @inject
    def __init__(self, ctx: Context):
        self.__ctx = ctx

    async def get_all(
        self,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[dict]:
        """社員一覧を取得する（キーワード検索・部署絞り込み対応）"""
        query = employees_table.select()

        # 部署での絞り込み
        if department:
            query = query.where(employees_table.c.department == department)

        # キーワード検索（氏名、社員番号、メールアドレスの部分一致）
        if keyword:
            pattern = f"%{keyword}%"
            query = query.where(
                sqlalchemy.or_(
                    employees_table.c.name.like(pattern),
                    employees_table.c.employee_code.like(pattern),
                    employees_table.c.email.like(pattern),
                )
            )

        query = query.order_by(employees_table.c.id.asc())
        result = await self.__ctx.db.fetch_all(query)
        return [dict(r) for r in result]

    async def get_by_id(self, employee_id: int) -> Optional[dict]:
        """IDで社員を1件取得する"""
        query = employees_table.select().where(employees_table.c.id == employee_id)
        result = await self.__ctx.db.fetch_one(query)
        return dict(result) if result else None

    async def get_by_code(self, employee_code: str) -> Optional[dict]:
        """社員番号で社員を1件取得する"""
        query = employees_table.select().where(employees_table.c.employee_code == employee_code)
        result = await self.__ctx.db.fetch_one(query)
        return dict(result) if result else None

    async def get_by_email(self, email: str) -> Optional[dict]:
        """メールアドレスで社員を1件取得する"""
        query = employees_table.select().where(employees_table.c.email == email)
        result = await self.__ctx.db.fetch_one(query)
        return dict(result) if result else None

    async def create(self, employee: EmployeeCreate) -> dict:
        """社員を新規登録する"""
        values = employee.model_dump()
        values["created_at"] = datetime.utcnow()
        values["updated_at"] = datetime.utcnow()
        query = employees_table.insert().values(**values)
        record_id = await self.__ctx.db.execute(query)
        created = await self.get_by_id(record_id)
        return created

    async def update(
        self,
        employee_id: int,
        employee: EmployeeUpdate,
    ) -> Optional[dict]:
        """社員情報を更新する"""
        update_data = employee.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(employee_id)

        update_data["updated_at"] = datetime.utcnow()
        query = (
            employees_table.update()
            .where(employees_table.c.id == employee_id)
            .values(**update_data)
        )
        await self.__ctx.db.execute(query)
        return await self.get_by_id(employee_id)

    async def delete(self, employee_id: int) -> bool:
        """社員を物理削除する"""
        query = employees_table.delete().where(employees_table.c.id == employee_id)
        affected = await self.__ctx.db.execute(query)
        return bool(affected)
