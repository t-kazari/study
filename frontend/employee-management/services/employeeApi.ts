import axios from 'axios';
import {
  Employee,
  EmployeeCreateInput,
  EmployeeSearchParams,
  EmployeeUpdateInput,
} from '../types/employee';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/employees`,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 社員一覧を取得する（キーワード・部署絞り込み対応）
 */
export const fetchEmployees = async (
  params?: EmployeeSearchParams,
): Promise<Employee[]> => {
  // TODO: [課題1] axios で GET /api/employees を呼び出してください
  // const response = await apiClient.get<Employee[]>('', { params });
  // return response.data;
  return [];
};

/**
 * 社員詳細を取得する
 */
export const fetchEmployeeById = async (id: number): Promise<Employee> => {
  const response = await apiClient.get<Employee>(`/${id}`);
  return response.data;
};

/**
 * 社員を新規登録する
 */
export const createEmployee = async (
  data: EmployeeCreateInput,
): Promise<Employee> => {
  // TODO: [課題2] axios で POST /api/employees を呼び出してください
  // const response = await apiClient.post<Employee>('', data);
  // return response.data;
  throw new Error('Not implemented');
};

/**
 * 社員情報を更新する（行内編集の保存）
 */
export const updateEmployee = async (
  id: number,
  data: EmployeeUpdateInput,
): Promise<Employee> => {
  // TODO: [課題3] axios で PUT /api/employees/{id} を呼び出してください
  // const response = await apiClient.put<Employee>(`/${id}`, data);
  // return response.data;
  throw new Error('Not implemented');
};

/**
 * 社員を物理削除する
 */
export const deleteEmployee = async (id: number): Promise<void> => {
  // TODO: [課題4] axios で DELETE /api/employees/{id} を呼び出してください
  // await apiClient.delete(`/${id}`);
  throw new Error('Not implemented');
};
