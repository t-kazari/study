# 【課題2】新規登録モーダル・バリデーションの実装

## 1. 目的
「新規社員登録」ボタンを押した際にモーダルダイアログ（MUI Dialog）を表示し、フォーム入力・バリデーション・バックエンドAPI経由でのDB登録・一覧の再描画を行う機能を実装します。

---

## 2. 達成要件
1. **フロントエンド (Next.js)**:
   - 「新規社員登録」ボタンを押すと、`EmployeeCreateModal` が開く。
   - **React Hook Form** と **Yup** を連携させ、以下の入力バリデーションを行う。
     - `employee_code`: 必須、半角英数字3〜10文字
     - `name`: 必須、50文字以内
     - `email`: 必須、メールアドレス形式
     - `department`: 必須（セレクト選択）
     - `position`: 必須（セレクト選択）
     - `joined_date`: 必須（日付）
     - `status`: 必須（セレクト選択）
   - バリデーションエラー時は対象項目の直下に赤字でエラーメッセージを表示する。
   - 送信成功時、モーダルを閉じて「社員◯◯を登録しました」とスナックバーで通知し、一覧を再取得して最新化する。
2. **バックエンド (FastAPI)**:
   - `POST /api/employees` エンドポイントを実装する。
   - 社員番号（`employee_code`）およびメールアドレス（`email`）が既に登録されていないか重複チェックを行い、重複している場合は `400 Bad Request` を返す。
   - 正常に登録された場合は `201 Created` と登録された社員オブジェクトを返す。

---

## 3. API仕様書

### `POST /api/employees`
- **リクエストボディ (JSON)**:
  ```json
  {
    "employee_code": "EMP010",
    "name": "東京 一郎",
    "email": "tokyo.ichiro@example.com",
    "department": "開発部",
    "position": "一般",
    "joined_date": "2026-04-01",
    "status": "在籍"
  }
  ```
- **成功レスポンス (201 Created)**: 登録された社員データのJSON
- **エラーレスポンス (400 Bad Request)**:
  ```json
  {
    "detail": "社員番号 'EMP010' は既に登録されています"
  }
  ```

---

## 4. 実装対象ファイルと実装手順

### バックエンド
1. **`infra/employee_impl.py`**:
   - `EmployeeRepositoryImpl.create()` を実装（`db.add`, `db.commit`, `db.refresh`）。
   - `get_by_code()`, `get_by_email()` を実装。
2. **`usecase/employee_service.py`**:
   - `create_employee()` メソッドで、重複チェック（`HTTPException(status_code=400)`）を行い、リポジトリの `create` を呼び出す。
3. **`handler/employee_handler.py`**:
   - `@router.post("", status_code=201)` を実装。

### フロントエンド
1. **`services/employeeApi.ts`**:
   - `createEmployee(data: EmployeeCreateInput)` を実装（`axios.post`）。
2. **`pages/components/EmployeeCreateModal.tsx`**:
   - `yup.object()` でバリデーションスキーマを定義。
   - `useForm` に `yupResolver` を渡し、MUIの各入力欄を `Controller` でバインド。
3. **`pages/EmployeeManagementUi.tsx`**:
   - `handleCreate` 関数で `createEmployee` を呼び出し、一覧を更新。

---

## 💡 実装のヒント & 参考コード

### フロントエンド: React Hook Form + Controller + MUI Select
```tsx
<Controller
  name="department"
  control={control}
  render={({ field }) => (
    <FormControl fullWidth size="small" error={Boolean(errors.department)}>
      <InputLabel id="dept-label">部署</InputLabel>
      <Select {...field} labelId="dept-label" label="部署">
        {DEPARTMENTS.map((dept) => (
          <MenuItem key={dept} value={dept}>{dept}</MenuItem>
        ))}
      </Select>
      {errors.department && <FormHelperText>{errors.department.message}</FormHelperText>}
    </FormControl>
  )}
/>
```

### バックエンド: 重複チェックの例外送出
```python
if self.repository.get_by_code(db, employee_data.employee_code):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"社員番号 '{employee_data.employee_code}' は既に登録されています",
    )
```
