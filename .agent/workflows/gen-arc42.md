---
description: 
---

# Generate arc42 Architecture Document

產生當前專案的 arc42 架構文件第一版草稿。

---

## Instructions

你是一位資深軟體架構師，請先向使用者逐條詢問以下資訊，收到回答後再開始分析原始碼與產生文件。

## 第一步：逐條詢問以下問題

請一次問完，讓使用者逐條回答：

1. **正式機網址**：專案是否已上線？若是，請提供正式機網址；若否，請提供測試機網址（或兩者都提供）
2. **部署環境**：主機環境為何？（例如：IIS 單機、Docker、Dokploy、雲端服務等，DB 是否同機？）
3. **外部串接**：系統有無串接第三方服務？（例如：金流、SMS、外部 API 等，若無請說無）
4. **文件受眾**：這份文件主要給誰看？（預設為新進工程師與 PM，可直接按 Enter 跳過）

## 第二步：分析原始碼

收到使用者回答後，依序執行：

1. 掃描專案根目錄結構，理解整體模組切分
2. 讀取依賴設定檔確認技術棧，優先尋找以下檔案：
   - .NET 專案：`packages.config`、`.csproj`、`Web.config`
   - Node 專案：`package.json`
   - Java 專案：`pom.xml`、`build.gradle`
   - 其他框架依此類推
3. 找到主要進入點、路由設定、API handler（含 `.ashx`）
4. 掃描資料模型與 DB 相關設定或 migration 檔案
5. 查看部署相關設定（Dockerfile、IIS config、CI/CD 設定等）

## 第三步：產生文件

- 在專案根目錄建立 `arc42/` 資料夾
- 每個章節輸出為獨立 `.md` 檔
- 所有內容以**繁體中文**撰寫
- 以受眾視角撰寫，避免未解釋的縮寫
- 無法從原始碼推斷的內容，標示 `<!-- TODO: 需人工補充 -->` 而非自行猜測

## 輸出檔案清單

| 檔名                             | 章節名稱       |
| -------------------------------- | -------------- |
| `01_introduction_and_goals.md`   | 簡介與目標     |
| `02_architecture_constraints.md` | 架構限制       |
| `03_system_scope_and_context.md` | 系統範疇與情境 |
| `04_solution_strategy.md`        | 解決方案策略   |
| `05_building_block_view.md`      | 建構區塊視圖   |
| `06_runtime_view.md`             | 執行期視圖     |
| `07_deployment_view.md`          | 部署視圖       |
| `08_crosscutting_concepts.md`    | 橫切關注點     |
| `09_architecture_decisions.md`   | 架構決策       |
| `10_quality_requirements.md`     | 品質需求       |
| `11_risks_and_technical_debt.md` | 風險與技術債   |
| `12_glossary.md`                 | 詞彙表         |

## 各章節產生原則

**第 2 章**：列出所有架構限制，包含：

- 技術限制（若偵測到 ASP.NET WebForms，須明確記載「技術棧為舊式 WebForms，非 MVC 或現代框架」）
- 資安要求（如 CDN 資源需下載本地、無對外 API 等）
- 組織限制（如機房部署、單機架構等）

**第 3 章**：產生系統情境圖，包含使用者、本系統、外部系統的邊界，使用 Mermaid 圖

**第 5 章**：產生主要模組與元件關係圖，使用 Mermaid 圖

**第 7 章**：根據部署環境描述拓樸，使用 Mermaid 圖呈現主機、服務、DB 的關係；若同時有測試機與正式機，分開描述兩套環境

**第 9 章**：從程式碼推斷重要架構決策，以 ADR 格式呈現：

```
### ADR-001 標題
- **狀態**：已採用
- **背景**：...
- **決策**：...
- **後果**：...
```

**第 11 章**：誠實列出觀察到的技術債與潛在風險，不美化

**第 12 章**：整理專案中出現的領域術語、技術縮寫與專有名詞

## 第四步：建立基準點

所有章節產生完畢後，執行以下動作：

1. 執行 `git rev-parse HEAD` 取得當前 commit hash
2. 將以下內容寫入 `arc42/.arc42-baseline`：

```
generated_at: <今天日期，格式 YYYY-MM-DD>
baseline_commit: <commit hash>
```

## 完成後輸出摘要

請輸出一份摘要，包含：

1. 偵測到的技術棧清單
2. 各章節的 TODO 數量統計
3. 建議優先人工補充的章節（前 3 名）
4. 已寫入 `arc42/.arc42-baseline` 的 baseline commit hash
