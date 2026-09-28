from abc import ABC, abstractmethod
from typing import List, Optional
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(ABC):
    """社員リポジトリの抽象基底クラス（インターフェース）"""

    @abstractmethod
    async def get_all(
        self,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[dict]:
        """社員一覧を取得する（キーワード検索・部署絞り込み対応）"""
        pass

    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Optional[dict]:
        """IDで社員を1件取得する"""
        pass

    @abstractmethod
    async def get_by_code(self, employee_code: str) -> Optional[dict]:
        """社員番号で社員を1件取得する"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[dict]:
        """メールアドレスで社員を1件取得する"""
        pass

    @abstractmethod
    async def create(self, employee: EmployeeCreate) -> dict:
        """社員を新規登録する"""
        pass

    @abstractmethod
    async def update(self, employee_id: int, employee: EmployeeUpdate) -> Optional[dict]:
        """社員情報を更新する"""
        pass

    @abstractmethod
    async def delete(self, employee_id: int) -> bool:
        """社員を物理削除する"""
        pass
