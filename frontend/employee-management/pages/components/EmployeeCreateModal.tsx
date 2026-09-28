import React from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import { Controller, useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import {
  DEPARTMENTS,
  EmployeeCreateInput,
  POSITIONS,
  STATUSES,
} from '../../types/employee';

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: EmployeeCreateInput) => Promise<void>;
}

// TODO: [課題2] Yup によるバリデーションスキーマを定義してください
// 1. employee_code: 必須、半角英数字3〜10文字 (matches)
// 2. name: 必須、最大50文字
// 3. email: 必須、メールアドレス形式 (email)
// 4. department, position, joined_date, status: 必須
const validationSchema: yup.ObjectSchema<EmployeeCreateInput> = yup.object({
  employee_code: yup.string().required('社員番号は必須です'),
  name: yup.string().required('氏名は必須です'),
  email: yup.string().required('メールアドレスは必須です'),
  department: yup.string().required('部署を選択してください'),
  position: yup.string().required('役職を選択してください'),
  joined_date: yup.string().required('入社日を入力してください'),
  status: yup.string().required('在籍ステータスを選択してください'),
});

const defaultValues: EmployeeCreateInput = {
  employee_code: '',
  name: '',
  email: '',
  department: '開発部',
  position: '一般',
  joined_date: new Date().toISOString().split('T')[0],
  status: '在籍',
};

export const EmployeeCreateModal: React.FC<Props> = ({
  open,
  onClose,
  onSubmit,
}) => {
  // TODO: [課題2] useForm に yupResolver(validationSchema) を設定してください
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<EmployeeCreateInput>({
    resolver: yupResolver(validationSchema),
    defaultValues,
  });

  const handleClose = () => {
    reset(defaultValues);
    onClose();
  };

  // TODO: [課題2] フォーム送信ハンドラーを実装してください
  // 1. await onSubmit(data); で親コンポーネントの登録処理を呼び出します。
  // 2. reset(defaultValues); でフォームを初期化します。
  // 3. onClose(); でモーダルを閉じます。
  const handleFormSubmit = async (data: EmployeeCreateInput) => {
    await onSubmit(data);
    reset(defaultValues);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ fontWeight: 'bold' }}>新規社員登録</DialogTitle>
      <form onSubmit={handleSubmit(handleFormSubmit)}>
        <DialogContent dividers>
          <Grid container spacing={2}>
            {/* 社員番号 */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="employee_code"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="社員番号"
                    placeholder="例: EMP010"
                    fullWidth
                    size="small"
                    error={Boolean(errors.employee_code)}
                    helperText={errors.employee_code?.message}
                  />
                )}
              />
            </Grid>

            {/* 氏名 */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="name"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="氏名"
                    placeholder="例: 田中 太郎"
                    fullWidth
                    size="small"
                    error={Boolean(errors.name)}
                    helperText={errors.name?.message}
                  />
                )}
              />
            </Grid>

            {/* メールアドレス */}
            <Grid item xs={12}>
              <Controller
                name="email"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="メールアドレス"
                    placeholder="例: tanaka.taro@example.com"
                    type="email"
                    fullWidth
                    size="small"
                    error={Boolean(errors.email)}
                    helperText={errors.email?.message}
                  />
                )}
              />
            </Grid>

            {/* 部署 */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="department"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth size="small" error={Boolean(errors.department)}>
                    <InputLabel id="create-dept-label">部署</InputLabel>
                    <Select {...field} labelId="create-dept-label" label="部署">
                      {DEPARTMENTS.map((dept) => (
                        <MenuItem key={dept} value={dept}>
                          {dept}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.department && (
                      <FormHelperText>{errors.department.message}</FormHelperText>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            {/* 役職 */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="position"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth size="small" error={Boolean(errors.position)}>
                    <InputLabel id="create-pos-label">役職</InputLabel>
                    <Select {...field} labelId="create-pos-label" label="役職">
                      {POSITIONS.map((pos) => (
                        <MenuItem key={pos} value={pos}>
                          {pos}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.position && (
                      <FormHelperText>{errors.position.message}</FormHelperText>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            {/* 入社日 */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="joined_date"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="入社日"
                    type="date"
                    fullWidth
                    size="small"
                    InputLabelProps={{ shrink: true }}
                    error={Boolean(errors.joined_date)}
                    helperText={errors.joined_date?.message}
                  />
                )}
              />
            </Grid>

            {/* 在籍ステータス */}
            <Grid item xs={12} sm={6}>
              <Controller
                name="status"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth size="small" error={Boolean(errors.status)}>
                    <InputLabel id="create-status-label">在籍ステータス</InputLabel>
                    <Select
                      {...field}
                      labelId="create-status-label"
                      label="在籍ステータス"
                    >
                      {STATUSES.map((st) => (
                        <MenuItem key={st} value={st}>
                          {st}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.status && (
                      <FormHelperText>{errors.status.message}</FormHelperText>
                    )}
                  </FormControl>
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ px: 3, py: 2 }}>
          <Button onClick={handleClose} color="inherit" disabled={isSubmitting}>
            キャンセル
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? '登録中...' : '登録する'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};
