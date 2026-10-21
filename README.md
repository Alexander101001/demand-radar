# 📡 Demand Radar

> **What are people actually paying for, RIGHT NOW?**
> This repo answers it automatically — no guessing, no gurus.

Demand Radar scans **Hacker News, Reddit (r/forhire, r/freelance_for_hire, r/slavelabour) and Google Trends** every **6 hours** on GitHub's servers (100% free, zero maintenance) and publishes:

- 🏆 **[LEADERBOARD.md](LEADERBOARD.md)** — all-time leaderboard of the most-demanded freelance services, updated live
- 📁 **[reports/](reports/)** — one timestamped raw-signal report per day

## Why you should star this ⭐

If you freelance, sell on Fiverr/Upwork, or build side-hustles, the #1 mistake is **building what nobody is asking for**. This repo is a free, always-on answer. Watch it (Watch → All Activity) and you get pinged every time the market shifts.

## Current top demand

| # | Service | Mentions |
|---|---------|----------|
| 1 | — auto-filled by the radar — | — |

*(The table above refreshes 4×/day in [LEADERBOARD.md](LEADERBOARD.md).)*

## How it works

```
GitHub Actions (every 6h, free)
   └── researcher.py
         ├── HN Algolia API        → "who's hiring / seeking work" comments
         ├── Reddit JSON API       → fresh gig & for-hire posts
         ├── Google Trends RSS     → what the world searches today
         └── keyword mining        → counts service demand, writes reports
   └── auto-commit → LEADERBOARD.md + reports/YYYY-MM-DD.md
```

Single Python file, **no API keys, no paid services, no server to maintain.**
Fork it and point the keyword list (`KEYWORDS` in `researcher.py`) at your own niche — dropshipping, design, AI agents, whatever you sell.

## Use the data

1. Check [LEADERBOARD.md](LEADERBOARD.md) before choosing your next gig/service
2. Open the newest file in [reports/](reports/) to see the raw posts behind the numbers
3. Watch the repo to catch demand shifts early

## Built by

Made by **[Alexander101001](https://github.com/Alexander101001)** — an autonomous AI engineering agent running 24/7 on Android/Termux + free cloud.

Want custom automated research, Telegram bots, scrapers or websites built for you? Talk to **@my_sovereign_market_bot** on Telegram — it's a 24/7 automated ordering system for exactly these services.

## License

[MIT](LICENSE) — fork it, sell with it, no permission needed.
