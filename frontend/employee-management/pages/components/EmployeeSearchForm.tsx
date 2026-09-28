import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  TextField,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AddIcon from '@mui/icons-material/Add';
import ClearIcon from '@mui/icons-material/Clear';
import { DEPARTMENTS, EmployeeSearchParams } from '../../types/employee';

interface Props {
  onSearch: (params: EmployeeSearchParams) => void;
  onOpenCreateModal: () => void;
}

export const EmployeeSearchForm: React.FC<Props> = ({
  onSearch,
  onOpenCreateModal,
}) => {
  const [keyword, setKeyword] = useState('');
  const [department, setDepartment] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      keyword: keyword.trim() || undefined,
      department: department || undefined,
    });
  };

  const handleClear = () => {
    setKeyword('');
    setDepartment('');
    onSearch({});
  };

  return (
    <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
      <Box component="form" onSubmit={handleSearch}>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={2}
          alignItems="center"
          justifyContent="space-between"
        >
          {/* 検索入力欄エリア */}
          <Stack
            direction={{ xs: 'column', sm: 'row' }}
            spacing={2}
            sx={{ flex: 1, width: '100%' }}
          >
            <TextField
              size="small"
              label="キーワード（氏名・社員番号・メール）"
              variant="outlined"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              sx={{ minWidth: 260 }}
            />

            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel id="search-department-label">部署</InputLabel>
              <Select
                labelId="search-department-label"
                value={department}
                label="部署"
                onChange={(e) => setDepartment(e.target.value)}
              >
                <MenuItem value="">すべて</MenuItem>
                {DEPARTMENTS.map((dept) => (
                  <MenuItem key={dept} value={dept}>
                    {dept}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              type="submit"
              variant="contained"
              startIcon={<SearchIcon />}
              sx={{ whiteSpace: 'nowrap' }}
            >
              検索
            </Button>
            <Button
              type="button"
              variant="outlined"
              color="inherit"
              startIcon={<ClearIcon />}
              onClick={handleClear}
              sx={{ whiteSpace: 'nowrap' }}
            >
              クリア
            </Button>
          </Stack>

          {/* 新規登録ボタン */}
          <Button
            type="button"
            variant="contained"
            color="success"
            startIcon={<AddIcon />}
            onClick={onOpenCreateModal}
            sx={{ whiteSpace: 'nowrap', mt: { xs: 2, sm: 0 } }}
          >
            新規社員登録
          </Button>
        </Stack>
      </Box>
    </Paper>
  );
};
