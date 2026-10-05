import React from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Typography,
} from '@mui/material';
import { Employee } from '../../types/employee';

interface Props {
  open: boolean;
  employee: Employee | null;
  loading: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
}

export const EmployeeDeleteConfirmDialog: React.FC<Props> = ({
  open,
  employee,
  loading,
  onClose,
  onConfirm,
}) => {
  if (!employee) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="xs" fullWidth>
      <DialogTitle sx={{ fontWeight: 'bold', color: 'error.main' }}>
        社員データの削除確認
      </DialogTitle>
      <DialogContent>
        <DialogContentText component="div">
          以下の社員情報を完全に削除します。よろしいですか？
          <Typography
            sx={{
              mt: 2,
              p: 1.5,
              backgroundColor: '#fbe9e7',
              borderRadius: 1,
              fontWeight: 500,
            }}
          >
            【{employee.employee_code}】 {employee.name}（{employee.department}）
          </Typography>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
            ※この操作を実行するとデータベースから物理的に削除され、元に戻すことはできません。
          </Typography>
        </DialogContentText>
      </DialogContent>
      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose} color="inherit" disabled={loading}>
          キャンセル
        </Button>
        <Button
          onClick={onConfirm}
          variant="contained"
          color="error"
          disabled={loading}
        >
          {loading ? '削除中...' : '削除する'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
