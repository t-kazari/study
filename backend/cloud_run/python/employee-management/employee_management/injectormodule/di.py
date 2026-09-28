from injector import Binder, Injector, Module, singleton
from employee_management.infra.employee_impl import EmployeeRepositoryImpl
from employee_management.repository.employee_repository import EmployeeRepository
from employee_management.usecase.employee_service import EmployeeService


class AppModule(Module):
    """依存性の注入（DI）設定モジュール"""

    def configure(self, binder: Binder) -> None:
        # EmployeeRepository（抽象インターフェース）に対して EmployeeRepositoryImpl（具象実装）をバインド
        binder.bind(EmployeeRepository, to=EmployeeRepositoryImpl, scope=singleton)
        binder.bind(EmployeeService, to=EmployeeService, scope=singleton)


# DIコンテナのグローバルインスタンスを生成
injector = Injector([AppModule()])


def get_employee_service() -> EmployeeService:
    """FastAPI の Depends で利用するサービス取得用ヘルパー関数"""
    return injector.get(EmployeeService)
