#!/usr/bin/env python3
"""
Cloud Researcher — runs on GitHub Actions (free servers, off-phone).
Scans free public sources for HIGH-DEMAND freelance/service opportunities,
then writes reports/YYYY-MM-DD.md which the phone engine pulls via git.
Sources: HN Algolia API, Reddit JSON, Google Trends RSS — all auth-free.
"""
import json, re, urllib.request, datetime, pathlib, html

UA = {"User-Agent": "Mozilla/5.0 (research-bot)"}
OUT = pathlib.Path("reports")
OUT.mkdir(exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "ignore")

def try_json(url):
    try:
        return json.loads(get(url))
    except Exception:
        return None

def clean(s):
    return html.unescape(re.sub(r"\s+", " ", s).strip())[:160]

ideas = []          # list of (source, text)
services_demand = {} # service keyword -> mention count

KEYWORDS = ["scraping", "web scraping", "telegram bot", "automation",
            "landing page", "dashboard", "qr code", "data entry",
            "excel", "python script", "ai agent", "seo", "email template"]

def mine(text, source):
    t = text.lower()
    for kw in KEYWORDS:
        if kw in t:
            services_demand[kw] = services_demand.get(kw, 0) + 1

# --- Source 1: Hacker News "who is hiring / freelance" via Algolia ---
d = try_json('https://hn.algolia.com/api/v1/search?query=%22freelance%22&tags=comment&hitsPerPage=30')
if d:
    for h in d.get("hits", []):
        txt = h.get("comment_text") or ""
        if len(txt) > 40:
            ideas.append(("Hacker News", clean(txt)))
            mine(txt, "HN")

# --- Source 2: Reddit r/forhire + r/freelance (JSON, public) ---
for sub in ["forhire", "freelance_for_hire", "slavelabour"]:
    d = try_json(f"https://www.reddit.com/r/{sub}/new.json?limit=25")
    if d:
        for c in d.get("data", {}).get("children", []):
            p = c.get("data", {})
            title = p.get("title", "")
            if title:
                ideas.append((f"reddit/r/{sub}", clean(title)))
                mine(title + " " + p.get("selftext", ""), sub)

# --- Source 3: Google Trends daily RSS (what the world searches today) ---
try:
    rss = get("https://trends.google.com/trending/rss?geo=US")
    topics = re.findall(r"<title>(.*?)</title>", rss)[1:20]
    for t in topics:
        ideas.append(("Google Trends", clean(t)))
except Exception:
    pass

# --- Build report ---
today = datetime.date.today().isoformat()
top_demand = sorted(services_demand.items(), key=lambda x: -x[1])[:8]
lines = [f"# Money Research Report — {today}",
         f"Sources scanned: HN, Reddit (forhire/freelance), Google Trends",
         f"Signals found: {len(ideas)}\n",
         "## Top in-demand services right now (highest first)\n"]
for kw, n in top_demand:
    lines.append(f"- SERVICE '{kw}' — {n} mentions today → sell this on Fiverr/Gumroad")
if not top_demand:
    lines.append("- No strong keyword signal today; default winners: telegram bots, scraping, landing pages")
lines.append("\n## Raw signals (latest 15)\n")
for src, txt in ideas[:15]:
    lines.append(f"- [{src}] {txt}")

report = "\n".join(lines)
path = OUT / f"{today}.md"
path.write_text(report)
print(f"wrote {path} ({len(ideas)} ideas, top demand: {top_demand[:3]})")

# --- Live LEADERBOARD.md at repo root (the front page hook) ---
ALL_TIME = pathlib.Path("LEADERBOARD.md")
old = {}
if ALL_TIME.exists():
    m = re.findall(r"\| (\d+) \| ([^|]+) \| (\d+) \|", ALL_TIME.read_text())
    for _, svc, total in m:
        old[svc.strip()] = int(total)
for kw, n in services_demand.items():
    old[kw] = old.get(kw, 0) + n
board = sorted(old.items(), key=lambda x: -x[1])[:10]
rows = "\n".join(f"| {i+1} | {svc.title()} | {tot} |" for i, (svc, tot) in enumerate(board))
ALL_TIME.write_text(
    f"# 🏆 All-Time Demand Leaderboard\n\n"
    f"Mentions of freelance services across HN + Reddit + Google Trends,\n"
    f"accumulated automatically 4×/day by GitHub Actions.\n\n"
    f"Last update: **{today}**\n\n"
    f"| # | Service | Mentions |\n|---|---------|----------|\n{rows}\n\n"
    f"→ Full history in [`reports/`](reports/)\n")
print(f"leaderboard updated: {board[:5]}")
