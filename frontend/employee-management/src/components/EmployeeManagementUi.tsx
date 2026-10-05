import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Alert,
  Box,
  Container,
  Snackbar,
  Typography,
} from '@mui/material';
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import {
  Employee,
  EmployeeCreateInput,
  EmployeeSearchParams,
  EmployeeUpdateInput,
} from '../../types/employee';
import { EmployeeSearchForm } from './EmployeeSearchForm';
import { EmployeeTable } from './EmployeeTable';
import { EmployeeCreateModal } from './EmployeeCreateModal';
import { EmployeeDeleteConfirmDialog } from './EmployeeDeleteConfirmDialog';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export const EmployeeManagementUi: React.FC = () => {
  // 社員一覧データ
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchParams, setSearchParams] = useState<EmployeeSearchParams>({});

  // モーダル・ダイアログの開閉状態
  const [createModalOpen, setCreateModalOpen] = useState<boolean>(false);
  const [deleteTargetEmployee, setDeleteTargetEmployee] = useState<Employee | null>(null);
  const [deleteLoading, setDeleteLoading] = useState<boolean>(false);

  // 通知スナックバー
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: 'success' | 'error' | 'info';
  }>({
    open: false,
    message: '',
    severity: 'info',
  });

  // 社員一覧データの取得 (axios 直接呼び出し)
  const loadEmployees = async (params: EmployeeSearchParams = searchParams) => {
    try {
      setLoading(true);
      const response = await axios.get<Employee[]>(`${API_BASE_URL}/api/employees`, {
        params,
      });
      setEmployees(response.data);
    } catch (err: any) {
      console.error('社員データ取得エラー:', err);
      showSnackbar('社員データの取得に失敗しました', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEmployees();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const showSnackbar = (message: string, severity: 'success' | 'error' | 'info') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar((prev) => ({ ...prev, open: false }));
  };

  // 検索ハンドラー
  const handleSearch = (params: EmployeeSearchParams) => {
    setSearchParams(params);
    loadEmployees(params);
  };

  // 新規社員登録ハンドラー (axios 直接呼び出し)
  const handleCreate = async (data: EmployeeCreateInput) => {
    try {
      await axios.post(`${API_BASE_URL}/api/employees`, data);
      showSnackbar(`社員「${data.name}」を登録しました`, 'success');
      await loadEmployees();
    } catch (err: any) {
      console.error('社員登録エラー:', err);
      const errorMsg =
        err.response?.data?.detail || '社員登録処理に失敗しました';
      showSnackbar(`登録失敗: ${errorMsg}`, 'error');
      throw err;
    }
  };

  // 行内編集・更新ハンドラー (axios 直接呼び出し)
  const handleUpdate = async (id: number, data: EmployeeUpdateInput) => {
    try {
      await axios.put(`${API_BASE_URL}/api/employees/${id}`, data);
      showSnackbar('社員情報を更新しました', 'success');
      await loadEmployees();
    } catch (err: any) {
      console.error('社員更新エラー:', err);
      const errorMsg =
        err.response?.data?.detail || '社員更新処理に失敗しました';
      showSnackbar(`更新失敗: ${errorMsg}`, 'error');
      throw err;
    }
  };

  // 削除ダイアログ開く
  const handleOpenDeleteDialog = (employee: Employee) => {
    setDeleteTargetEmployee(employee);
  };

  // 削除実行ハンドラー (axios 直接呼び出し)
  const handleConfirmDelete = async () => {
    if (!deleteTargetEmployee) return;

    try {
      setDeleteLoading(true);
      await axios.delete(`${API_BASE_URL}/api/employees/${deleteTargetEmployee.id}`);
      showSnackbar(`社員「${deleteTargetEmployee.name}」を削除しました`, 'success');
      setDeleteTargetEmployee(null);
      await loadEmployees();
    } catch (err: any) {
      console.error('社員削除エラー:', err);
      const errorMsg =
        err.response?.data?.detail || '社員削除処理に失敗しました';
      showSnackbar(`削除失敗: ${errorMsg}`, 'error');
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* 画面タイトル */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <PeopleAltIcon sx={{ fontSize: 36, color: 'primary.main', mr: 1.5 }} />
        <Typography variant="h4" component="h1" fontWeight="bold">
          社員名簿管理システム
        </Typography>
      </Box>

      {/* 検索・新規登録エリア */}
      <EmployeeSearchForm
        onSearch={handleSearch}
        onOpenCreateModal={() => setCreateModalOpen(true)}
      />

      {/* 社員一覧テーブル */}
      <EmployeeTable
        employees={employees}
        loading={loading}
        onUpdate={handleUpdate}
        onOpenDeleteDialog={handleOpenDeleteDialog}
      />

      {/* 新規登録モーダル */}
      <EmployeeCreateModal
        open={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        onSubmit={handleCreate}
      />

      {/* 削除確認ダイアログ */}
      <EmployeeDeleteConfirmDialog
        open={Boolean(deleteTargetEmployee)}
        employee={deleteTargetEmployee}
        loading={deleteLoading}
        onClose={() => setDeleteTargetEmployee(null)}
        onConfirm={handleConfirmDelete}
      />

      {/* 操作通知スナックバー */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbar.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default EmployeeManagementUi;
