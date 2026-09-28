export interface Employee {
  id: number;
  employee_code: string;
  name: string;
  email: string;
  department: string;
  position: string;
  joined_date: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreateInput {
  employee_code: string;
  name: string;
  email: string;
  department: string;
  position: string;
  joined_date: string;
  status: string;
}

export interface EmployeeUpdateInput {
  name?: string;
  email?: string;
  department?: string;
  position?: string;
  joined_date?: string;
  status?: string;
}

export interface EmployeeSearchParams {
  keyword?: string;
  department?: string;
}

export const DEPARTMENTS = ['開発部', '営業部', '人事部', '総務部'] as const;
export const POSITIONS = ['一般', 'リーダー', 'マネージャー', '部長'] as const;
export const STATUSES = ['在籍', '休職', '退職'] as const;
