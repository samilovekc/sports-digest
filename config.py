"""新聞主題設定。想增減關鍵字，只需要改這個檔案。

每個 topic:
  name : 顯示用名稱
  q    : Google News 搜尋語法（支援 OR、"精確詞組"、-排除詞）
  lang : zh（繁中/台灣）、en（美國英文）、ja（日文）
  max  : 每次最多取幾則（預設 MAX_PER_TOPIC）
section 的順序 = 去重優先順序（同一則新聞只會出現在最先符合的區塊）。
"""

WINDOW = "2d"          # 每次抓取回溯多久（抓取每天跑多次，重複的會自動去重）
MAX_PER_TOPIC = 8

# 標題含這些字的新聞會加上 ⭐ 並在區塊內置頂
PIN_PATTERN = r"Royals|皇家|Kansas City|KC "

SECTIONS = [
    {"id": "royals", "title": "⭐ 堪薩斯皇家", "topics": [
        {"name": "Royals 英文", "q": '"Kansas City Royals"', "lang": "en", "max": 10},
        {"name": "皇家 中文", "q": "堪薩斯皇家", "lang": "zh"},
        {"name": "Royals 簽約/交易", "q": 'Royals (signs OR trade OR "free agent" OR extension)', "lang": "en"},
        {"name": "Royals 傷病", "q": 'Royals (injury OR "injured list" OR surgery)', "lang": "en"},
    ]},
    {"id": "bb_fa", "title": "⚾ 美日台 自由球員 / 重大簽約", "topics": [
        {"name": "MLB FA", "q": 'MLB "free agent" (signs OR agrees OR contract)', "lang": "en"},
        {"name": "MLB 中文", "q": "大聯盟 自由球員 簽約", "lang": "zh"},
        {"name": "NPB FA", "q": "プロ野球 FA 移籍 OR 入団 OR 契約更改", "lang": "ja"},
        {"name": "NPB 旅美", "q": "ポスティング メジャー 挑戦", "lang": "ja"},
        {"name": "日職 中文", "q": "日職 自由球員 OR 旅美 OR 契約", "lang": "zh"},
        {"name": "中職 FA", "q": "中職 自由球員 OR 簽約 OR 續約", "lang": "zh"},
    ]},
    {"id": "bb_injury", "title": "🩹 棒球傷病更新", "topics": [
        {"name": "MLB 傷病", "q": 'MLB (injury OR "injured list" OR surgery) update', "lang": "en"},
        {"name": "NPB 傷病", "q": "プロ野球 故障 OR 離脱 OR 手術", "lang": "ja"},
        {"name": "台灣球員傷病", "q": "旅外 OR 中職 球員 傷兵 OR 受傷 OR 開刀", "lang": "zh"},
    ]},
    {"id": "bb_venue", "title": "🏟️ 棒球場館進度", "topics": [
        {"name": "Royals 新球場", "q": 'Royals (stadium OR ballpark) Kansas City Jackson County', "lang": "en", "max": 6},
        {"name": "MLB 球場", "q": 'MLB (ballpark OR stadium) (construction OR relocation OR financing) -football', "lang": "en"},
        {"name": "台灣球場", "q": "棒球場 OR 大巨蛋 興建 OR 啟用 OR 進度", "lang": "zh"},
        {"name": "日本球場", "q": "新球場 プロ野球 建設", "lang": "ja"},
    ]},
    {"id": "mlb_cba", "title": "🤝 MLB 勞資協議（CBA）", "topics": [
        {"name": "CBA 英文", "q": 'MLB (CBA OR lockout OR "salary cap" OR MLBPA OR "collective bargaining")', "lang": "en", "max": 12},
        {"name": "勞資 中文", "q": "大聯盟 勞資協議 OR 封館 OR 薪資上限", "lang": "zh"},
    ]},
    {"id": "nba_rec", "title": "🏀 NBA 球星與紀錄", "topics": [
        {"name": "NBA 紀錄", "q": 'NBA (record OR milestone OR "triple-double" OR "career-high")', "lang": "en"},
        {"name": "NBA 中文", "q": "NBA 紀錄 OR 大三元 OR 生涯新高", "lang": "zh"},
    ]},
    {"id": "nba_injury", "title": "🩹 NBA 傷病", "topics": [
        {"name": "NBA 傷病", "q": 'NBA injury (out OR "ruled out" OR surgery OR return)', "lang": "en"},
        {"name": "NBA 傷病 中文", "q": "NBA 傷病 OR 缺陣 OR 復出", "lang": "zh"},
    ]},
    {"id": "celtics", "title": "☘️ 賽爾提克", "topics": [
        {"name": "Celtics", "q": '"Boston Celtics"', "lang": "en", "max": 10},
        {"name": "塞爾提克", "q": "塞爾提克", "lang": "zh"},
    ]},
    {"id": "nfl_race", "title": "🏈 NFL 季後賽席次爭奪", "topics": [
        {"name": "Playoff picture", "q": '"NFL playoff picture" OR "wild card race" OR "clinch playoff"', "lang": "en", "max": 10},
        {"name": "NFL 中文", "q": "NFL 季後賽 席次 OR 戰績 OR 外卡", "lang": "zh"},
    ]},
    {"id": "nfl_venue", "title": "🏟️ NFL 場館進度", "topics": [
        {"name": "NFL 新球場", "q": 'NFL (stadium OR dome) (construction OR relocation OR financing) Chiefs OR Bears OR Browns OR Commanders', "lang": "en"},
        {"name": "Chiefs 新球場", "q": "Chiefs Kansas stadium", "lang": "en", "max": 6},
    ]},
    {"id": "other", "title": "🌐 其他運動重點", "topics": [
        {"name": "F1", "q": "F1 Grand Prix", "lang": "en", "max": 5},
        {"name": "網球", "q": "ATP OR WTA tennis", "lang": "en", "max": 5},
        {"name": "NHL", "q": "NHL", "lang": "en", "max": 5},
        {"name": "足球", "q": "Premier League OR Champions League OR 世足", "lang": "zh", "max": 6},
        {"name": "台灣運動", "q": "台灣 選手 國際賽 OR 金牌 OR 羽球 OR 籃球 TPBL OR T1", "lang": "zh", "max": 8},
        {"name": "格鬥/其他", "q": "UFC OR 奧運", "lang": "zh", "max": 4},
    ]},
    {"id": "world", "title": "🌍 世界要聞", "topics": [
        {"name": "國際頭條", "topic_feed": "WORLD", "lang": "zh", "max": 10},
        {"name": "台灣頭條", "topic_feed": "NATION", "lang": "zh", "max": 8},
    ]},
]
