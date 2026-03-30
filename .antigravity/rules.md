# 專案任務 (Mission)
這是一個基於 Python 的「員工打卡與 AI 查詢系統」。
包含 Web 介面（上下班打卡、午休紀錄）以及一個右下角的懸浮聊天室（整合 Google Gemini 進行 RAG 查詢）。

# 開發與架構規範
1. 框架選擇：使用 FastAPI 作為後端，前端使用 Jinja2 模板與 Bootstrap 5。
2. 資料庫：使用 PostgreSQL，並透過 SQLAlchemy 進行非同步 (Async) 的 ORM 操作。
3. AI 整合：使用 `google-genai` 或 LangChain 串接 Gemini API。查詢出勤紀錄時，必須先從資料庫撈取該員工的紀錄，將結果轉為文字 Context 後，再交由 Gemini 生成自然語言回覆（RAG 架構）。
4. 安全與隔離（絕對遵守）：
   - 開發環境必須完全基於 Docker。
   - 所有 Python 相依套件必須寫在 `requirements.txt` 中，不允許在主機全域環境安裝套件。
   - 不要執行任何具破壞性的系統指令（如 rm -rf 等）。
5. 程式碼風格：
   - 變數與函式命名請使用 snake_case。
   - 加上適當的 Type Hints（型別提示）與繁體中文註解。