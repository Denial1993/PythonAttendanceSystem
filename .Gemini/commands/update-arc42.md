# /update-arc42

檢查近期 git commit，判斷 `arc42/` 是否需要更新，並直接修改受影響的章節。

## 執行步驟

1. 執行 `git log --oneline -30`，列出近 30 筆 commit
2. 讀取 `arc42/.arc42-baseline`，取得 `baseline_commit`；
   若檔案不存在則取最近 10 筆 commit
3. 對每筆相關 commit 執行 `git show --stat <hash>`，確認異動檔案清單
4. 對影響架構的異動執行 `git diff <hash>~ <hash> -- <檔案路徑>`，閱讀實際變更內容
5. 依下方對應規則判斷影響章節
6. 直接修改 `arc42/` 對應檔案
7. 報告：修改了哪些章節、原因是什麼；哪些 commit 判斷為不影響文件
8. 更新 `arc42/.arc42-baseline`：
   - `baseline_commit` 改為當前 HEAD（執行 `git rev-parse HEAD` 取得）
   - `generated_at` 改為今天日期（格式 YYYY-MM-DD）

## 異動 → 章節對應規則

| 異動類型                                                   | 需更新章節                             |
| ---------------------------------------------------------- | -------------------------------------- |
| 新增 `.ashx` handler                                       | 第 3 章（外部介面）、第 5 章（模組圖） |
| 新增外部 API 呼叫、硬碼 URL                                | 第 3 章                                |
| `Web.config` 設定異動（session、timeout、customErrors 等） | 第 7 章、第 8 章                       |
| 新增重大資料夾或模組（大量新頁面）                         | 第 5 章、第 6 章                       |
| 認證 / 授權邏輯異動                                        | 第 8 章、第 9 章（ADR）、第 10 章      |
| 引入新 NuGet 套件（packages.config）                       | 第 4 章、第 8 章                       |
| 引入新 npm 套件（package.json）                            | 第 4 章                                |
| 修正已知技術債（第 11 章列出的項目）                       | 第 11 章                               |
| 部署相關異動（路徑、IIS 設定）                             | 第 7 章                                |
| 新增加密 / 金鑰邏輯                                        | 第 8 章、第 9 章                       |
| 新增領域實體或術語                                         | 第 12 章（詞彙表）                     |

## 不需更新的異動

- 一般 bug fix（業務邏輯修正，未改變架構）
- UI 文字、樣式微調
- SQL 查詢優化（無新資料表或欄位）
- 既有模組的小功能擴充（不引入新外部依賴、不改變模組邊界）
- 測試資料、暫存檔清理

## 文件位置

`arc42/` 下共 12 個章節檔案與 1 個基準檔：

- `.arc42-baseline`
- `01_introduction_and_goals.md`
- `02_architecture_constraints.md`
- `03_system_scope_and_context.md`
- `04_solution_strategy.md`
- `05_building_block_view.md`
- `06_runtime_view.md`
- `07_deployment_view.md`
- `08_crosscutting_concepts.md`
- `09_architecture_decisions.md`
- `10_quality_requirements.md`
- `11_risks_and_technical_debt.md`
- `12_glossary.md`
