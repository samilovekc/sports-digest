# 每日運動・世界新聞摘要

自動抓取 Google News，依「台北日期」整理成手機友善網頁。免費、不需主機、不需你在線。

## 一次性設定（約 10 分鐘，入伍前做完）
1. 在 GitHub 建一個新 repo（Public 才能免費用 Pages），把本資料夾內容全部上傳。
2. Settings → Actions → General → Workflow permissions 選 **Read and write permissions**。
3. Actions 分頁 → daily-digest → **Run workflow** 手動跑第一次（會建立 docs/ 與資料）。
4. Settings → Pages → Source 選 **Deploy from a branch**，Branch 選 `main` / `/docs`。
5. 取得網址（`https://<帳號>.github.io/<repo>/`），手機「加入主畫面」。

之後每天台北 06:00、14:00、22:00 自動更新；新聞依發布日存成 `docs/data/YYYY-MM-DD.json`，永久累積。

## 使用
- 預設顯示最新一天；上方按鈕可切「昨天／近 3 天／近 7 天／全部」，或自選日期區間。
- 區塊標籤可只看單一主題；搜尋框可找球員/球隊。
- 「標記看到此日」會記住進度，下次出現「未讀（某日之後）」一鍵補看（存在該瀏覽器，換手機會重來）。
- 皇家相關新聞有 ⭐，區塊內置頂。

## 終端機補看（本機有 Python 3 即可）
    python digest.py print --since 2026-12-01 --until 2026-12-05 > recap.md

## 客製
所有關鍵字都在 `config.py`（英/日/繁中查詢可自由增減）。改完 commit 即生效。
`python digest.py demo` 可用假資料預覽版面（預覽後請刪除 docs/data 再正式跑）。

## 注意
- 資料來自 Google News RSS：只有標題、媒體、時間，需點進原文；英日文標題不會翻譯。
- 搜尋式新聞會有雜訊，關鍵字可再微調（如加 `-排除詞`）。
- GitHub 對 60 天沒有 repo 活動的排程會停用；本程式每次有新資料都會 commit，通常算活動，
  但建議服役約第 50 天請家人/自己確認 Actions 還在跑。
- 抓取有重複去重，但同一事件不同媒體仍會各列一則。
