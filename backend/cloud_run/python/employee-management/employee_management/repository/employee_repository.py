from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from employee_management.domain.employee import EmployeeCreate, EmployeeUpdate


class EmployeeRepository(ABC):
    """社員リポジトリの抽象基底クラス（インターフェース）"""

    @abstractmethod
    def get_all(
        self,
        db: Session,
        keyword: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[any]:
        """社員一覧を取得する（キーワード検索・部署絞り込み対応）"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, employee_id: int) -> Optional[any]:
        """IDで社員を1件取得する"""
        pass

    @abstractmethod
    def get_by_code(self, db: Session, employee_code: str) -> Optional[any]:
        """社員番号で社員を1件取得する"""
        pass

    @abstractmethod
    def get_by_email(self, db: Session, email: str) -> Optional[any]:
        """メールアドレスで社員を1件取得する"""
        pass

    @abstractmethod
    def create(self, db: Session, employee: EmployeeCreate) -> any:
        """社員を新規登録する"""
        pass

    @abstractmethod
    def update(self, db: Session, employee_id: int, employee: EmployeeUpdate) -> Optional[any]:
        """社員情報を更新する"""
        pass

    @abstractmethod
    def delete(self, db: Session, employee_id: int) -> bool:
        """社員を物理削除する"""
        pass
