import React, { useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  Chip,
  FormControl,
  MenuItem,
  Paper,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from '@mui/material';
import SaveIcon from '@mui/icons-material/Save';
import DeleteIcon from '@mui/icons-material/Delete';
import {
  DEPARTMENTS,
  Employee,
  EmployeeUpdateInput,
  POSITIONS,
  STATUSES,
} from '../../types/employee';

interface Props {
  employees: Employee[];
  loading: boolean;
  onUpdate: (id: number, data: EmployeeUpdateInput) => Promise<void>;
  onOpenDeleteDialog: (employee: Employee) => void;
}

export const EmployeeTable: React.FC<Props> = ({
  employees,
  loading,
  onUpdate,
  onOpenDeleteDialog,
}) => {
  // チェックされている行のID群を管理
  const [checkedIds, setCheckedIds] = useState<number[]>([]);
  // 各行の編集中の入力値 { [employeeId]: Partial<Employee> }
  const [editRows, setEditRows] = useState<{ [id: number]: Partial<Employee> }>({});
  // 保存中の行ID
  const [savingId, setSavingId] = useState<number | null>(null);

  // チェックボックス切り替え時のハンドラー
  const handleToggleCheck = (employee: Employee) => {
    const isChecked = checkedIds.includes(employee.id);
    if (isChecked) {
      // チェック解除：選択リストから除外＆編集データを破棄
      setCheckedIds((prev) => prev.filter((id) => id !== employee.id));
      setEditRows((prev) => {
        const next = { ...prev };
        delete next[employee.id];
        return next;
      });
    } else {
      // チェックON：選択リストに追加＆現在値で初期化
      setCheckedIds((prev) => [...prev, employee.id]);
      setEditRows((prev) => ({
        ...prev,
        [employee.id]: {
          name: employee.name,
          email: employee.email,
          department: employee.department,
          position: employee.position,
          joined_date: employee.joined_date,
          status: employee.status,
        },
      }));
    }
  };

  // 入力フィールド変更時のハンドラー
  const handleFieldChange = (
    employeeId: number,
    field: keyof Employee,
    value: string,
  ) => {
    setEditRows((prev) => ({
      ...prev,
      [employeeId]: {
        ...prev[employeeId],
        [field]: value,
      },
    }));
  };

  // 更新保存ハンドラー
  const handleSave = async (id: number) => {
    const editData = editRows[id];
    if (!editData) return;

    try {
      setSavingId(id);
      await onUpdate(id, editData);
      // 保存完了後にチェック解除
      setCheckedIds((prev) => prev.filter((i) => i !== id));
      setEditRows((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
    } finally {
      setSavingId(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case '在籍':
        return 'success';
      case '休職':
        return 'warning';
      case '退職':
        return 'default';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography color="text.secondary">データを読み込み中...</Typography>
      </Paper>
    );
  }

  if (employees.length === 0) {
    return (
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography color="text.secondary">対象の社員データが見つかりませんでした。</Typography>
      </Paper>
    );
  }

  return (
    <TableContainer component={Paper} elevation={1}>
      <Table sx={{ minWidth: 950 }} size="small">
        <TableHead sx={{ backgroundColor: '#f0f4f8' }}>
          <TableRow>
            <TableCell width={60} align="center">編集</TableCell>
            <TableCell width={110}>社員番号</TableCell>
            <TableCell width={160}>氏名</TableCell>
            <TableCell width={220}>メールアドレス</TableCell>
            <TableCell width={130}>部署</TableCell>
            <TableCell width={120}>役職</TableCell>
            <TableCell width={130}>入社日</TableCell>
            <TableCell width={110}>ステータス</TableCell>
            <TableCell width={170} align="center">操作</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {employees.map((emp) => {
            const isChecked = checkedIds.includes(emp.id);
            const currentEdit = editRows[emp.id] || {};
            const isSaving = savingId === emp.id;

            return (
              <TableRow
                key={emp.id}
                hover
                sx={{
                  backgroundColor: isChecked ? '#f0f9ff' : 'inherit',
                  transition: 'background-color 0.2s',
                }}
              >
                {/* 活性化切り替えチェックボックス */}
                <TableCell align="center">
                  <Checkbox
                    checked={isChecked}
                    onChange={() => handleToggleCheck(emp)}
                    size="small"
                  />
                </TableCell>

                {/* 社員番号（常に読み取り専用） */}
                <TableCell sx={{ fontWeight: 600 }}>{emp.employee_code}</TableCell>

                {/* 氏名 */}
                <TableCell>
                  {isChecked ? (
                    <TextField
                      size="small"
                      fullWidth
                      value={currentEdit.name ?? emp.name}
                      onChange={(e) => handleFieldChange(emp.id, 'name', e.target.value)}
                    />
                  ) : (
                    emp.name
                  )}
                </TableCell>

                {/* メールアドレス */}
                <TableCell>
                  {isChecked ? (
                    <TextField
                      size="small"
                      type="email"
                      fullWidth
                      value={currentEdit.email ?? emp.email}
                      onChange={(e) => handleFieldChange(emp.id, 'email', e.target.value)}
                    />
                  ) : (
                    emp.email
                  )}
                </TableCell>

                {/* 部署 */}
                <TableCell>
                  {isChecked ? (
                    <FormControl size="small" fullWidth>
                      <Select
                        value={currentEdit.department ?? emp.department}
                        onChange={(e) =>
                          handleFieldChange(emp.id, 'department', e.target.value)
                        }
                      >
                        {DEPARTMENTS.map((dept) => (
                          <MenuItem key={dept} value={dept}>
                            {dept}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ) : (
                    emp.department
                  )}
                </TableCell>

                {/* 役職 */}
                <TableCell>
                  {isChecked ? (
                    <FormControl size="small" fullWidth>
                      <Select
                        value={currentEdit.position ?? emp.position}
                        onChange={(e) =>
                          handleFieldChange(emp.id, 'position', e.target.value)
                        }
                      >
                        {POSITIONS.map((pos) => (
                          <MenuItem key={pos} value={pos}>
                            {pos}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ) : (
                    emp.position
                  )}
                </TableCell>

                {/* 入社日 */}
                <TableCell>
                  {isChecked ? (
                    <TextField
                      size="small"
                      type="date"
                      fullWidth
                      value={currentEdit.joined_date ?? emp.joined_date}
                      onChange={(e) =>
                        handleFieldChange(emp.id, 'joined_date', e.target.value)
                      }
                    />
                  ) : (
                    emp.joined_date
                  )}
                </TableCell>

                {/* 在籍ステータス */}
                <TableCell>
                  {isChecked ? (
                    <FormControl size="small" fullWidth>
                      <Select
                        value={currentEdit.status ?? emp.status}
                        onChange={(e) =>
                          handleFieldChange(emp.id, 'status', e.target.value)
                        }
                      >
                        {STATUSES.map((st) => (
                          <MenuItem key={st} value={st}>
                            {st}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ) : (
                    <Chip
                      label={emp.status}
                      size="small"
                      color={getStatusColor(emp.status)}
                    />
                  )}
                </TableCell>

                {/* 操作ボタン列（チェックOFF時は非活性） */}
                <TableCell align="center">
                  <Stack direction="row" spacing={1} justifyContent="center">
                    <Button
                      size="small"
                      variant="contained"
                      color="primary"
                      startIcon={<SaveIcon />}
                      disabled={!isChecked || isSaving}
                      onClick={() => handleSave(emp.id)}
                    >
                      {isSaving ? '保存中' : '保存'}
                    </Button>
                    <Button
                      size="small"
                      variant="outlined"
                      color="error"
                      startIcon={<DeleteIcon />}
                      disabled={!isChecked || isSaving}
                      onClick={() => onOpenDeleteDialog(emp)}
                    >
                      削除
                    </Button>
                  </Stack>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
