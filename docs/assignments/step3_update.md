# 【課題3】行内編集・チェックボックス活性化制御の実装

## 1. 目的
社員一覧テーブルの各行にある「チェックボックス」と連動し、チェックされた行の各カラムを入力フォーム（TextField / Select）に切り替えて活性化し、行右端の「保存」ボタンから更新API（PUT）を実行してDBデータを更新する機能を実装します。

---

## 2. 達成要件
1. **フロントエンド (Next.js)**:
   - 各レコードの左端にチェックボックス（デフォルトはOFF）を配置する。
   - **チェックOFF時**:
     - 氏名、メール、部署、役職、入社日、ステータスは通常テキストで表示。
     - 行右端の「保存」「削除」ボタンは `disabled`（非活性）状態。
   - **チェックON時**:
     - 該当行の背景色を強調（ハイライト）。
     - 各列が入力フォーム（TextField / Select）に変化し、編集可能になる。
     - 行右端の「保存」ボタンが活性化。
   - 「保存」ボタン押下時:
     - バックエンドの `PUT /api/employees/{id}` を呼び出し、更新に成功したらチェックを解除して一覧を再取得する。
2. **バックエンド (FastAPI)**:
   - `PUT /api/employees/{id}` エンドポイントを実装する。
   - 指定IDの社員が存在しない場合は `404 Not Found` を返す。
   - メールアドレスを変更した場合、他の社員が既に使用しているメールなら `400 Bad Request` を返す。
   - 更新に成功したら `200 OK` と更新後の社員オブジェクトを返す。

---

## 3. API仕様書

### `PUT /api/employees/{employee_id}`
- **パスパラメータ**: `employee_id` (int, 必須)
- **リクエストボディ (JSON)**:
  ```json
  {
    "name": "山田 太郎（更新後）",
    "email": "yamada.updated@example.com",
    "department": "営業部",
    "position": "マネージャー",
    "joined_date": "2021-04-01",
    "status": "在籍"
  }
  ```
- **成功レスポンス (200 OK)**: 更新された社員オブジェクト

---

## 4. 実装対象ファイルと実装手順

### バックエンド
1. **`infra/employee_impl.py`**:
   - `EmployeeRepositoryImpl.update()` を実装。
   - `model_dump(exclude_unset=True)` で渡された項目のみモデル属性に代入し、`db.commit()` と `db.refresh()` を実行。
2. **`usecase/employee_service.py`**:
   - `update_employee()` メソッドを実装。
   - 存在チェック（404）およびメールアドレスの重複チェック（400）を行う。
3. **`handler/employee_handler.py`**:
   - `@router.put("/{employee_id}")` ハンドラーを実装。

### フロントエンド
1. **`services/employeeApi.ts`**:
   - `updateEmployee(id: number, data: EmployeeUpdateInput)` を実装（`axios.put`）。
2. **`pages/components/EmployeeTable.tsx`**:
   - `checkedIds`（チェックされた社員ID配列）ステートと、`editRows`（編集内容の辞書）ステートを管理。
   - `isChecked ? <TextField ... /> : emp.name` のように三項演算子で表示を切り替える。
   - 「保存」ボタンの `disabled={!isChecked}` 制御を実装。

---

## 💡 実装のヒント & 参考コード

### フロントエンド: チェック状態に応じた条件分岐レンダリング
```tsx
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
```

### バックエンド: 部分更新のSQLAlchemy Core + Context実装
```python
async def update(self, employee_id: int, employee: EmployeeUpdate):
    update_data = employee.model_dump(exclude_unset=True)
    if not update_data:
        return await self.get_by_id(employee_id)

    update_data["updated_at"] = datetime.utcnow()
    query = (
        employees_table.update()
        .where(employees_table.c.id == employee_id)
        .values(**update_data)
    )
    await self.__ctx.db.execute(query)
    return await self.get_by_id(employee_id)
```
