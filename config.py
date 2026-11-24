"""新聞主題設定。想增減關鍵字，只需要改這個檔案。

每個 topic:
  name : 顯示用名稱
  q    : Google News 搜尋語法（支援 OR、"精確詞組"、-排除詞）
  lang : zh（繁中/台灣）、en（美國英文）、ja（日文）
  max  : 每次最多取幾則（預設 MAX_PER_TOPIC）
  must : （選填）標題必須含其中任一個詞（正規表示式，用 | 分隔），否則丟棄
section 的順序 = 去重優先順序（同一則新聞只會出現在最先符合的區塊）。
"""

WINDOW = "2d"          # 每次抓取回溯多久（抓取每天跑多次，重複的會自動去重）
MAX_PER_TOPIC = 8

# 標題含這些字的新聞會加上 ⭐ 並在區塊內置頂
PIN_PATTERN = r"Royals|皇家|Kansas City|KC "

# 標題含這些字的新聞一律丟棄（只放把握高的詞，避免誤傷）
BLOCK_PATTERN = r"優惠碼|折扣碼|promo code|sportsbook|賠率|投注|博彩"

# ---- 共用隊名清單（供 must 使用）----
NBA_EN = (r"NBA|Hawks|Celtics|Nets|Hornets|Bulls|Cavaliers|Cavs|Mavericks|Mavs|Nuggets|Pistons|"
          r"Warriors|Rockets|Pacers|Clippers|Lakers|Grizzlies|Heat|Bucks|Timberwolves|Wolves|Pelicans|"
          r"Knicks|Thunder|Magic|76ers|Sixers|Suns|Blazers|Kings|Spurs|Raptors|Jazz|Wizards")
NBA_ZH = (r"NBA|老鷹|塞爾提克|賽爾提克|籃網|黃蜂|公牛|騎士|獨行俠|金塊|活塞|勇士|火箭|溜馬|快艇|湖人|"
          r"灰熊|熱火|公鹿|灰狼|鵜鶘|尼克|雷霆|魔術|76人|太陽|拓荒者|國王|馬刺|暴龍|爵士|巫師")
MLB_EN = (r"MLB|baseball|Diamondbacks|Braves|Orioles|Red Sox|Cubs|White Sox|Reds|Guardians|Rockies|Tigers|"
          r"Astros|Royals|Angels|Dodgers|Marlins|Brewers|Twins|Mets|Yankees|Athletics|Phillies|Pirates|"
          r"Padres|Giants|Mariners|Cardinals|Rays|Rangers|Blue Jays|Nationals")
NPB_JA = (r"プロ野球|NPB|巨人|阪神|DeNA|ヤクルト|広島|中日|ソフトバンク|日本ハム|ロッテ|楽天|オリックス|西武")
CPBL_ZH = r"中職|統一|樂天|富邦|味全|中信|台鋼|兄弟"

SECTIONS = [
    {"id": "royals", "title": "⭐ 堪薩斯皇家", "topics": [
        {"name": "Royals 英文", "q": '"Kansas City Royals"', "lang": "en", "max": 10, "must": r"Royals|Kansas City|KC "},
        {"name": "皇家 中文", "q": "堪薩斯皇家", "lang": "zh", "must": r"皇家|堪薩斯|Royals"},
        {"name": "Royals 簽約/交易", "q": 'Royals (signs OR trade OR "free agent" OR extension)', "lang": "en", "must": r"Royals|Kansas City"},
        {"name": "Royals 傷病", "q": 'Royals (injury OR "injured list" OR surgery)', "lang": "en", "must": r"Royals|Kansas City"},
    ]},
    {"id": "bb_fa", "title": "⚾ 美日台 自由球員 / 重大簽約", "topics": [
        {"name": "MLB FA", "q": 'MLB "free agent" (signs OR agrees OR contract)', "lang": "en", "must": MLB_EN},
        {"name": "MLB 中文", "q": "大聯盟 自由球員 簽約", "lang": "zh", "must": r"大聯盟|MLB|美職|棒|皇家|道奇|洋基"},
        {"name": "NPB FA", "q": "プロ野球 FA 移籍 OR 入団 OR 契約更改", "lang": "ja", "must": NPB_JA},
        {"name": "NPB 旅美", "q": "ポスティング メジャー 挑戦", "lang": "ja", "must": r"メジャー|MLB|ポスティング"},
        {"name": "日職 中文", "q": "日職 自由球員 OR 旅美 OR 契約", "lang": "zh", "must": r"日職|日本職棒|NPB|讀賣|巨人|阪神|軟銀|火腿|羅德|歐力士|西武|養樂多|廣島|中日|橫濱|旅美|大聯盟"},
        {"name": "中職 FA", "q": "中職 自由球員 OR 簽約 OR 續約", "lang": "zh", "must": CPBL_ZH},
    ]},
    {"id": "bb_injury", "title": "🩹 棒球傷病更新", "topics": [
        {"name": "MLB 傷病", "q": 'MLB (injury OR "injured list" OR surgery) update', "lang": "en", "must": MLB_EN},
        {"name": "NPB 傷病", "q": "プロ野球 故障 OR 離脱 OR 手術", "lang": "ja", "must": NPB_JA},
        {"name": "台灣球員傷病", "q": "旅外 OR 中職 球員 傷兵 OR 受傷 OR 開刀", "lang": "zh", "must": CPBL_ZH + r"|旅外|旅美|旅日|棒球"},
    ]},
    {"id": "bb_venue", "title": "🏟️ 棒球場館進度", "topics": [
        {"name": "Royals 新球場", "q": 'Royals (stadium OR ballpark) Kansas City Jackson County', "lang": "en", "max": 6, "must": r"Royals|Kansas City|Jackson County"},
        {"name": "MLB 球場", "q": 'MLB (ballpark OR stadium) (construction OR relocation OR financing) -football', "lang": "en", "must": MLB_EN + r"|ballpark"},
        {"name": "台灣球場", "q": "棒球場 OR 大巨蛋 興建 OR 啟用 OR 進度", "lang": "zh", "must": r"棒球|大巨蛋|中職"},
        {"name": "日本球場", "q": "新球場 プロ野球 建設", "lang": "ja", "must": r"野球|ボールパーク|球場"},
    ]},
    {"id": "mlb_cba", "title": "🤝 MLB 勞資協議（CBA）", "topics": [
        {"name": "CBA 英文", "q": 'MLB (CBA OR lockout OR "salary cap" OR MLBPA OR "collective bargaining")', "lang": "en", "max": 12, "must": r"MLB|baseball|Manfred|MLBPA|Players Association"},
        {"name": "勞資 中文", "q": "大聯盟 勞資協議 OR 封館 OR 薪資上限", "lang": "zh", "must": r"大聯盟|MLB|棒球|球員工會"},
    ]},
    {"id": "nba_rec", "title": "🏀 NBA 球星與紀錄", "topics": [
        {"name": "NBA 紀錄", "q": 'NBA (record OR milestone OR "triple-double" OR "career-high")', "lang": "en", "must": NBA_EN},
        {"name": "NBA 中文", "q": "NBA 紀錄 OR 大三元 OR 生涯新高", "lang": "zh", "must": NBA_ZH},
    ]},
    {"id": "nba_injury", "title": "🩹 NBA 傷病", "topics": [
        {"name": "NBA 傷病", "q": 'NBA injury (out OR "ruled out" OR surgery OR return)', "lang": "en", "must": NBA_EN},
        {"name": "NBA 傷病 中文", "q": "NBA 傷病 OR 缺陣 OR 復出", "lang": "zh", "must": NBA_ZH},
    ]},
    {"id": "celtics", "title": "☘️ 塞爾提克", "topics": [
        {"name": "Celtics", "q": '"Boston Celtics"', "lang": "en", "max": 10, "must": r"Celtics|Boston"},
        {"name": "塞爾提克", "q": "塞爾提克 OR 賽爾提克", "lang": "zh", "must": r"塞爾提克|賽爾提克|綠衫軍|Celtics"},
    ]},
    {"id": "nfl_race", "title": "🏈 NFL 季後賽席次爭奪", "topics": [
        {"name": "Playoff picture", "q": '"NFL playoff picture" OR "wild card race" OR "clinch playoff"', "lang": "en", "max": 10, "must": r"NFL|playoff|wild card|AFC|NFC"},
        {"name": "NFL 中文", "q": "NFL 季後賽 席次 OR 戰績 OR 外卡", "lang": "zh", "must": r"NFL|美式足球|季後賽|AFC|NFC"},
    ]},
    {"id": "nfl_venue", "title": "🏟️ NFL 場館進度", "topics": [
        {"name": "NFL 新球場", "q": 'NFL (stadium OR dome) (construction OR relocation OR financing) Chiefs OR Bears OR Browns OR Commanders', "lang": "en", "must": r"NFL|Chiefs|Bears|Browns|Commanders|Arrowhead|Soldier Field"},
        {"name": "Chiefs 新球場", "q": "Chiefs Kansas stadium", "lang": "en", "max": 6, "must": r"Chiefs|Kansas|Arrowhead"},
    ]},
    {"id": "other", "title": "🌐 其他運動重點", "topics": [
        {"name": "F1", "q": "F1 Grand Prix", "lang": "en", "max": 5, "must": r"F1|Formula 1|Grand Prix"},
        {"name": "網球", "q": "ATP OR WTA tennis", "lang": "en", "max": 5, "must": r"ATP|WTA|tennis"},
        {"name": "NHL", "q": "NHL", "lang": "en", "max": 5, "must": r"NHL|Stanley Cup"},
        {"name": "足球", "q": "Premier League OR Champions League OR 世足", "lang": "zh", "max": 6},
        {"name": "台灣運動", "q": "台灣 選手 國際賽 OR 金牌 OR 羽球 OR 籃球 TPBL OR T1", "lang": "zh", "max": 8},
        {"name": "格鬥/其他", "q": "UFC OR 奧運", "lang": "zh", "max": 4},
    ]},
    {"id": "world", "title": "🌍 世界要聞", "topics": [
        {"name": "國際頭條", "topic_feed": "WORLD", "lang": "zh", "max": 10},
        {"name": "台灣頭條", "topic_feed": "NATION", "lang": "zh", "max": 8},
    ]},
]
