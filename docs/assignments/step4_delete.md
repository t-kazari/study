# 【課題4】削除機能の実装

## 1. 目的
社員一覧の各行に配置された「削除」ボタンから、誤削除を防止するための確認ダイアログ（MUI Dialog）を表示し、バックエンドの物理削除API（DELETE）を実行してDBから対象レコードを削除する機能を実装します。

---

## 2. 達成要件
1. **フロントエンド (Next.js)**:
   - 各行の右端にある「削除」ボタンは、チェックボックスがONの時のみ活性化（`disabled={!isChecked}`）される。
   - 「削除」ボタンを押すと、`EmployeeDeleteConfirmDialog` が開き、削除対象の社員番号と氏名が表示される。
   - 「キャンセル」を押すとダイアログが閉じる。
   - 「削除する」ボタンを押すと、バックエンドの `DELETE /api/employees/{id}` を呼び出す。
   - 削除完了後、ダイアログを閉じ、「社員◯◯を削除しました」とスナックバーで通知し、一覧データを再取得して表示から消去する。
2. **バックエンド (FastAPI)**:
   - `DELETE /api/employees/{employee_id}` エンドポイントを実装する。
   - 対象社員が存在しない場合は `404 Not Found` を返す。
   - 正常に削除された場合は HTTP ステータスコード `204 No Content` を返す。

---

## 3. API仕様書

### `DELETE /api/employees/{employee_id}`
- **パスパラメータ**: `employee_id` (int, 必須)
- **成功レスポンス (204 No Content)**: ボディなし
- **エラーレスポンス (404 Not Found)**:
  ```json
  {
    "detail": "社員ID: 999 が見つかりません"
  }
  ```

---

## 4. 実装対象ファイルと実装手順

### バックエンド
1. **`infra/employee_impl.py`**:
   - `EmployeeRepositoryImpl.delete()` を実装。
   - `db.delete(db_employee)` と `db.commit()` を実行。
2. **`usecase/employee_service.py`**:
   - `delete_employee()` メソッドを実装。
   - 存在チェック（404）を行い、リポジトリの `delete` を呼び出す。
3. **`handler/employee_handler.py`**:
   - `@router.delete("/{employee_id}", status_code=204)` ハンドラーを実装。

### フロントエンド
1. **`services/employeeApi.ts`**:
   - `deleteEmployee(id: number)` を実装（`axios.delete`）。
2. **`pages/components/EmployeeDeleteConfirmDialog.tsx`**:
   - 削除対象社員の情報を表示し、確認ボタンで `onConfirm` を実行。
3. **`pages/EmployeeManagementUi.tsx`**:
   - `handleConfirmDelete` 関数を実装し、`deleteEmployee` を呼び出して一覧を再取得。

---

## 💡 実装のヒント & 参考コード

### フロントエンド: axios による DELETE リクエスト
```typescript
export const deleteEmployee = async (id: number): Promise<void> => {
  await apiClient.delete(`/${id}`);
};
```

### バックエンド: 204 No Content のハンドラー定義
```python
@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="社員削除",
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    service: EmployeeService = Depends(get_employee_service),
):
    service.delete_employee(db, employee_id)
    return None
```
