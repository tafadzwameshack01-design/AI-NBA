# 🏀 CLUTCH v2 — NBA Intelligence System

> Multi-source AI predictions · Auto W/L grading · Live countdowns · Full transparency

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo, branch `main`, file `app.py`
4. Add secret in **Settings → Secrets** (optional):
   ```toml
   ODDS_API_KEY = "your_key_here"
   ```

## Data Sources
- ESPN Scoreboard & Schedules (live, no key needed)
- NBA Stats Advanced (ORTG, DRTG, PACE, eFG%, NET RTG)
- NBA Stats Base (PTS, REB, AST, FG%, W%)
- ESPN Injury Reports (real-time)
- The Odds API (optional — live spreads/totals)

## Prediction Types
- **Q1 Spread** — Which team wins the 1st quarter
- **Q1 Total OVER/UNDER** — Combined Q1 scoring
- **Moneyline** — Outright winner

## W/L Grading
Auto-grades against ESPN final scores. Hit **Grade Now** in the Results tab or wait for the 60-second auto-refresh.

## Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- Do NOT add `sqlite3` to requirements.txt (it's stdlib)
- Do NOT add `nba_api` — causes Streamlit Cloud failures
- Season constant in `app.py` line ~`SEASON = "2024-25"` — update each season
