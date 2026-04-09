# CLUTCH — NBA Intelligence System

Advanced AI-powered NBA predictions. Live data. Full transparency on W/L record.

## Data Sources
- ESPN Scoreboard API — live scores, injuries, embedded odds
- NBA Stats API — advanced metrics: ORTG, DRTG, Pace, eFG%, TS%, Net Rating
- NBA Stats Base — PTS, REB, AST, FG%, Win%
- ESPN Injuries — real-time injury reports
- The Odds API (optional) — spreads and totals

## Features
- Q1 Spread + Q1 Total predictions for every game
- Live tip-off countdown timers (CAT timezone)
- Animated UI — gradient header, glowing W/L badges, live pulse
- Full W/L record with streak tracking and per-bet-type breakdown
- Auto-grading engine — pending picks graded when games finish
- Team deep dive — advanced stats, last 10 games, Q1 chart
- 95%+ confidence signal amplification model

## Deploy (Streamlit Community Cloud)
1. Fork / push this repo to GitHub
2. Go to share.streamlit.io → New app → select repo → `app.py`
3. In App Settings → Secrets, add:
```
ODDS_API_KEY = "your_key_here"
```
4. Deploy — free tier works fine

## Local
```bash
pip install -r requirements.txt
streamlit run app.py
```
