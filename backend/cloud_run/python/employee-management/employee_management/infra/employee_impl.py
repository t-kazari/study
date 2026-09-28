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
        # TODO: [課題1] 社員一覧取得処理を実装してください
        # 1. query = employees_table.select() でセレクトクエリを作成します。
        # 2. department が指定されている場合は query.where(employees_table.c.department == department) を追加します。
        # 3. keyword が指定されている場合は sqlalchemy.or_() を使い、name, employee_code, email の部分一致（.like()）を追加します。
        # 4. query.order_by(employees_table.c.id.asc()) でソートします。
        # 5. result = await self.__ctx.db.fetch_all(query) で非同期取得し、[dict(r) for r in result] を返してください。
        pass

    async def get_by_id(self, employee_id: int) -> Optional[dict]:
        """IDで社員を1件取得する"""
        query = employees_table.select().where(employees_table.c.id == employee_id)
        result = await self.__ctx.db.fetch_one(query)
        return dict(result) if result else None

    async def get_by_code(self, employee_code: str) -> Optional[dict]:
        # TODO: [課題2] 社員番号での重複チェック用取得クエリを実装してください
        # 1. query = employees_table.select().where(employees_table.c.employee_code == employee_code)
        # 2. result = await self.__ctx.db.fetch_one(query)
        # 3. dict(result) または None を返してください
        pass

    async def get_by_email(self, email: str) -> Optional[dict]:
        # TODO: [課題2] メールアドレスでの重複チェック用取得クエリを実装してください
        # 1. query = employees_table.select().where(employees_table.c.email == email)
        # 2. result = await self.__ctx.db.fetch_one(query)
        # 3. dict(result) または None を返してください
        pass

    async def create(self, employee: EmployeeCreate) -> dict:
        # TODO: [課題2] 社員新規登録処理を実装してください
        # 1. values = employee.model_dump() で辞書化し、created_at, updated_at を追加します。
        # 2. query = employees_table.insert().values(**values)
        # 3. record_id = await self.__ctx.db.execute(query) でINSERTを実行して新規レコードIDを取得します。
        # 4. return await self.get_by_id(record_id) で登録データを返してください。
        pass

    async def update(
        self,
        employee_id: int,
        employee: EmployeeUpdate,
    ) -> Optional[dict]:
        # TODO: [課題3] 社員情報更新処理を実装してください
        # 1. update_data = employee.model_dump(exclude_unset=True) で渡された更新項目を取得します。
        # 2. update_data["updated_at"] = datetime.utcnow() を追加します。
        # 3. query = employees_table.update().where(employees_table.c.id == employee_id).values(**update_data)
        # 4. await self.__ctx.db.execute(query) でUPDATEを実行します。
        # 5. return await self.get_by_id(employee_id) で更新後データを返してください。
        pass

    async def delete(self, employee_id: int) -> bool:
        # TODO: [課題4] 社員の物理削除処理を実装してください
        # 1. query = employees_table.delete().where(employees_table.c.id == employee_id)
        # 2. affected = await self.__ctx.db.execute(query) でDELETEを実行します。
        # 3. return bool(affected)
        pass
