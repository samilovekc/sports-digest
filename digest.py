#!/usr/bin/env python3
"""每日運動/世界新聞摘要：抓取 Google News RSS → 依「台北日期」分檔 → 產生靜態網站。

用法：
  python digest.py              抓取 + 建置網站（GitHub Actions 用這個）
  python digest.py fetch        只抓取
  python digest.py build        只重建 docs/index.html 與日期索引
  python digest.py print --since 2026-12-01 [--until 2026-12-05]   在終端機輸出 Markdown
  python digest.py demo         產生假資料，用來預覽版面
只用 Python 標準函式庫，不需 pip install。
"""
import argparse, json, re, sys, hashlib, random
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta, date
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).parent))
from config import SECTIONS, WINDOW, MAX_PER_TOPIC, PIN_PATTERN  # noqa: E402

TZ = timezone(timedelta(hours=8))  # 台北時間
ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DATA = DOCS / "data"
LOCALES = {
    "zh": "hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "en": "hl=en-US&gl=US&ceid=US:en",
    "ja": "hl=ja&gl=JP&ceid=JP:ja",
}
UA = "Mozilla/5.0 (compatible; sports-digest/1.0)"


def feed_url(topic):
    loc = LOCALES[topic.get("lang", "zh")]
    if topic.get("topic_feed"):
        return f"https://news.google.com/rss/headlines/section/topic/{topic['topic_feed']}?{loc}"
    q = quote(f"{topic['q']} when:{WINDOW}")
    return f"https://news.google.com/rss/search?q={q}&{loc}"


def norm(title):
    return re.sub(r"[\W_]+", "", title.lower())[:80]


def parse_rss(xml_text):
    """回傳 [{t,u,s,p}]；title 尾端的「 - 媒體名」會被拆出。"""
    out = []
    root = ET.fromstring(xml_text)
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        src_el = it.find("source")
        source = (src_el.text or "").strip() if src_el is not None else ""
        if source and title.endswith(" - " + source):
            title = title[: -(len(source) + 3)].strip()
        elif " - " in title and not source:
            title, source = title.rsplit(" - ", 1)
        try:
            pub = parsedate_to_datetime(it.findtext("pubDate")).astimezone(TZ)
        except Exception:
            continue
        if title and link:
            out.append({"t": title, "u": link, "s": source, "p": pub.isoformat(timespec="minutes")})
    return out


def fetch_topic(args):
    sec, topic = args
    try:
        req = Request(feed_url(topic), headers={"User-Agent": UA})
        with urlopen(req, timeout=25) as r:
            items = parse_rss(r.read())
        items.sort(key=lambda x: x["p"], reverse=True)
        return sec, topic, items[: topic.get("max", MAX_PER_TOPIC)], None
    except Exception as e:  # 單一來源失敗不影響其他
        return sec, topic, [], f"{type(e).__name__}: {e}"


def load_day(d):
    f = DATA / f"{d}.json"
    return json.loads(f.read_text("utf-8")) if f.exists() else []


def save_day(d, items):
    items.sort(key=lambda x: x["p"], reverse=True)
    (DATA / f"{d}.json").write_text(json.dumps(items, ensure_ascii=False, separators=(",", ":")), "utf-8")


def fetch_all():
    DATA.mkdir(parents=True, exist_ok=True)
    jobs = [(s, t) for s in SECTIONS for t in s["topics"]]
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(fetch_topic, jobs))  # 保持 config 順序
    pin = re.compile(PIN_PATTERN, re.I)
    seen_run, by_day, errors, got = set(), {}, 0, 0
    for sec, topic, items, err in results:
        if err:
            errors += 1
            print(f"[warn] {sec['id']}/{topic['name']}: {err}", file=sys.stderr)
            continue
        for it in items:
            k = norm(it["t"])
            if k in seen_run:
                continue
            seen_run.add(k)
            it.update(c=sec["id"], n=topic["name"])
            if pin.search(it["t"]):
                it["pin"] = 1
            by_day.setdefault(it["p"][:10], []).append(it)
            got += 1
    added = 0
    for d, new in by_day.items():
        old = load_day(d)
        have = {norm(x["t"]) for x in old}
        fresh = [x for x in new if norm(x["t"]) not in have]
        if fresh:
            save_day(d, old + fresh)
            added += len(fresh)
    print(f"fetched {got} items, {added} new, {errors}/{len(jobs)} feeds failed")
    if errors == len(jobs):
        sys.exit("all feeds failed")


def build():
    DATA.mkdir(parents=True, exist_ok=True)
    days = []
    for f in sorted(DATA.glob("????-??-??.json"), reverse=True):
        days.append({"d": f.stem, "n": len(json.loads(f.read_text("utf-8")))})
    (DATA / "days.json").write_text(json.dumps(days), "utf-8")
    secs = [{"id": s["id"], "title": s["title"]} for s in SECTIONS]
    html = (ROOT / "template.html").read_text("utf-8").replace("__SECTIONS__", json.dumps(secs, ensure_ascii=False))
    html = html.replace("__BUILT__", datetime.now(TZ).strftime("%Y-%m-%d %H:%M"))
    (DOCS / "index.html").write_text(html, "utf-8")
    print(f"built site with {len(days)} days")


def print_md(since, until):
    until = until or date.today().isoformat()
    titles = {s["id"]: s["title"] for s in SECTIONS}
    order = [s["id"] for s in SECTIONS]
    for f in sorted(DATA.glob("????-??-??.json"), reverse=True):
        if not (since <= f.stem <= until):
            continue
        print(f"\n# {f.stem}")
        items = load_day(f.stem)
        for cid in order:
            rows = sorted((i for i in items if i["c"] == cid), key=lambda i: (not i.get("pin"), i["p"]), reverse=False)
            if rows:
                print(f"\n## {titles[cid]}")
                for i in rows:
                    print(f"- {'⭐ ' if i.get('pin') else ''}[{i['t']}]({i['u']}) — {i['s']} {i['p'][11:16]}")


def demo():
    DATA.mkdir(parents=True, exist_ok=True)
    random.seed(1)
    samples = ["示範標題：這裡會顯示真實新聞標題", "Demo headline: real news titles appear here", "デモ見出し：実際のニュース"]
    today = datetime.now(TZ)
    for back in range(5):
        d = (today - timedelta(days=back)).date().isoformat()
        items = []
        for s in SECTIONS:
            for j in range(random.randint(1, 4)):
                t = f"{random.choice(samples)} #{s['id']}-{j}"
                it = {"t": t, "u": "https://news.google.com/", "s": "Demo", "c": s["id"], "n": "demo",
                      "p": f"{d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}"}
                if s["id"] == "royals":
                    it["pin"] = 1
                items.append(it)
        save_day(d, items)
    print("demo data written")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="all", choices=["all", "fetch", "build", "print", "demo"])
    ap.add_argument("--since", default=(date.today() - timedelta(days=1)).isoformat())
    ap.add_argument("--until")
    a = ap.parse_args()
    if a.cmd == "demo":
        demo(); build()
    elif a.cmd == "fetch":
        fetch_all()
    elif a.cmd == "build":
        build()
    elif a.cmd == "print":
        print_md(a.since, a.until)
    else:
        fetch_all(); build()


if __name__ == "__main__":
    main()
