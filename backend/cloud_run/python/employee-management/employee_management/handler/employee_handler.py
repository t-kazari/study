from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from employee_management.domain.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from employee_management.injectormodule.di import get_employee_service
from employee_management.usecase.employee_service import EmployeeService
from employee_management.utils.contextutils import get_logger

logger = get_logger()

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("", response_model=List[EmployeeResponse], summary="社員一覧取得")
async def get_employees(
    keyword: Optional[str] = Query(None, description="キーワード検索（氏名、社員番号、メール）"),
    department: Optional[str] = Query(None, description="所属部署絞り込み"),
    service: EmployeeService = Depends(get_employee_service),
):
    """社員一覧を取得する（検索・絞り込み対応）"""
    logger.info(f"社員一覧取得リクエスト: keyword={keyword}, department={department}")
    return await service.get_employees(keyword=keyword, department=department)


@router.get("/{employee_id}", response_model=EmployeeResponse, summary="社員詳細取得")
async def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
):
    """指定IDの社員情報を取得する"""
    logger.info(f"社員詳細取得リクエスト: id={employee_id}")
    return await service.get_employee_by_id(employee_id)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="社員新規登録",
)
async def create_employee(
    employee_data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    """社員を新規登録する"""
    logger.info(f"社員新規登録リクエスト: code={employee_data.employee_code}, name={employee_data.name}")
    return await service.create_employee(employee_data)


@router.put("/{employee_id}", response_model=EmployeeResponse, summary="社員情報更新")
async def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service),
):
    """社員情報を更新する（行内編集の保存）"""
    logger.info(f"社員更新リクエスト: id={employee_id}")
    return await service.update_employee(employee_id, employee_data)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="社員削除",
)
async def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
):
    """社員を物理削除する"""
    logger.info(f"社員削除リクエスト: id={employee_id}")
    await service.delete_employee(employee_id)
    return None
