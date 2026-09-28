# 【課題1】社員一覧取得・検索機能の実装

## 1. 目的
データベースに保存されている社員データをバックエンドから取得し、フロントエンドのテーブル上に一覧表示する機能を実装します。また、キーワード検索と部署による絞り込み機能も作成します。

---

## 2. 達成要件
1. **バックエンド (FastAPI)**:
   - `GET /api/employees` エンドポイントを実装する。
   - クエリパラメータ `keyword`（氏名、社員番号、メールアドレスの部分一致）に対応する。
   - クエリパラメータ `department`（所属部署の完全一致）に対応する。
   - レスポンスとして社員リストのJSON（`List[EmployeeResponse]`）を返す。
2. **フロントエンド (Next.js)**:
   - `services/employeeApi.ts` で `GET /api/employees` を呼び出す `fetchEmployees` を実装する。
   - `pages/EmployeeManagementUi.tsx` で初期表示時にAPIを呼び出し、取得データを状態（state）にセットする。
   - `pages/components/EmployeeTable.tsx` で取得した社員データをMUI Tableで一覧表示する。
   - `pages/components/EmployeeSearchForm.tsx` で検索・クリアボタンが押された際に再取得を行う。

---

## 3. API仕様書

### `GET /api/employees`
- **クエリパラメータ**:
  - `keyword` (string, 任意): 氏名・社員番号・メールアドレスのLIKE検索
  - `department` (string, 任意): 部署名の完全一致
- **成功レスポンス (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "employee_code": "EMP001",
      "name": "山田 太郎",
      "email": "yamada.taro@example.com",
      "department": "開発部",
      "position": "リーダー",
      "joined_date": "2021-04-01",
      "status": "在籍",
      "created_at": "2026-04-01T09:00:00",
      "updated_at": "2026-04-01T09:00:00"
    }
  ]
  ```

---

## 4. 実装対象ファイルと実装手順

### バックエンド
1. **`infra/employee_impl.py`**:
   - `EmployeeRepositoryImpl.get_all()` メソッドを実装します。
   - SQLAlchemyの `select(EmployeeModel)` を使い、`keyword` と `department` の条件を追加して `db.scalars(query).all()` を返します。
2. **`usecase/employee_service.py`**:
   - `EmployeeService.get_employees()` メソッドを実装します。
   - インジェクションされた `self.repository.get_all(db, keyword, department)` を呼び出します。
3. **`handler/employee_handler.py`**:
   - `@router.get("")` に `get_employees` ハンドラーを実装し、クエリパラメータを受け取ってServiceを呼び出します。

### フロントエンド
1. **`services/employeeApi.ts`**:
   - `fetchEmployees(params?: EmployeeSearchParams)` を実装し、axios で `GET /api/employees` をリクエストします。
2. **`pages/EmployeeManagementUi.tsx`**:
   - `useEffect` フックで初回ロード時に `loadEmployees()` を呼び出し、結果を `setEmployees` に保存します。
   - 検索フォームから渡された検索パラメータで再度 `loadEmployees(params)` を呼び出す `handleSearch` を実装します。
3. **`pages/components/EmployeeTable.tsx`**:
   - `employees.map((emp) => ...)` で行（`TableRow`）をレンダリングします。

---

## 💡 実装のヒント & 参考コード

### バックエンドのヒント (SQLAlchemy 2.0の検索クエリ)
```python
from sqlalchemy import or_, select

query = select(EmployeeModel)
if department:
    query = query.where(EmployeeModel.department == department)
if keyword:
    pattern = f"%{keyword}%"
    query = query.where(
        or_(
            EmployeeModel.name.like(pattern),
            EmployeeModel.employee_code.like(pattern),
            EmployeeModel.email.like(pattern),
        )
    )
query = query.order_by(EmployeeModel.id.asc())
return list(db.scalars(query).all())
```

### フロントエンドのヒント (axios呼び出し)
```typescript
export const fetchEmployees = async (params?: EmployeeSearchParams): Promise<Employee[]> => {
  const response = await apiClient.get<Employee[]>('', { params });
  return response.data;
};
```
