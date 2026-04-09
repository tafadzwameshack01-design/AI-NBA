"""
╔══════════════════════════════════════════════════════════════╗
║              CLUTCH — NBA Intelligence System                ║
║  Advanced AI Predictions · Live Data · Full Transparency     ║
║  Sources: ESPN API · NBA Stats · BallDontLie · SportsPage   ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import sqlite3
import json
import pandas as pd
import numpy as np
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import time
from dataclasses import dataclass, field
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="CLUTCH · NBA Intelligence",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'About': 'CLUTCH — Precision NBA predictions. Data-driven. Transparent.'}
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS — Animations, Fonts, Theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

/* ── Reset & theme ─────────────────────────────────────── */
:root {
  --clutch-orange: #FF6B35;
  --clutch-gold: #FFB800;
  --clutch-green: #00E676;
  --clutch-red: #FF1744;
  --clutch-blue: #00B0FF;
  --bg-dark: #0A0A0F;
  --bg-card: #111118;
  --bg-surface: #1A1A24;
  --text-primary: #F0F0F5;
  --text-muted: #888899;
  --border: rgba(255,107,53,0.15);
}

/* ── Keyframe animations ───────────────────────────────── */
@keyframes headerPulse {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes slideInUp {
  from { transform: translateY(24px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}
@keyframes slideInLeft {
  from { transform: translateX(-20px); opacity: 0; }
  to   { transform: translateX(0);     opacity: 1; }
}
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 8px var(--clutch-green); }
  50%       { box-shadow: 0 0 24px var(--clutch-green), 0 0 48px rgba(0,230,118,0.3); }
}
@keyframes redGlow {
  0%, 100% { box-shadow: 0 0 8px var(--clutch-red); }
  50%       { box-shadow: 0 0 24px var(--clutch-red), 0 0 48px rgba(255,23,68,0.3); }
}
@keyframes livePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.6; transform: scale(1.05); }
}
@keyframes countdownTick {
  0%  { transform: scale(1); }
  10% { transform: scale(1.04); }
  20% { transform: scale(1); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}
@keyframes borderFlow {
  0%   { border-color: var(--clutch-orange); }
  33%  { border-color: var(--clutch-gold); }
  66%  { border-color: var(--clutch-blue); }
  100% { border-color: var(--clutch-orange); }
}

/* ── Hero header ───────────────────────────────────────── */
.clutch-hero {
  background: linear-gradient(135deg, #0A0A0F 0%, #1a0a00 30%, #0d0d1a 60%, #0A0A0F 100%);
  background-size: 300% 300%;
  animation: headerPulse 8s ease infinite;
  border-radius: 16px;
  padding: 32px 40px 24px;
  margin-bottom: 24px;
  border: 1px solid var(--border);
  position: relative;
  overflow: hidden;
}
.clutch-hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--clutch-orange), var(--clutch-gold), transparent);
  animation: shimmer 3s linear infinite;
  background-size: 200% auto;
}
.clutch-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 4rem;
  letter-spacing: 0.12em;
  background: linear-gradient(135deg, #FF6B35, #FFB800, #FF6B35);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 4s linear infinite;
  line-height: 1;
  margin: 0;
}
.clutch-sub {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-muted);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 6px;
}
.clutch-tagline {
  font-family: 'Inter', sans-serif;
  font-weight: 300;
  font-size: 0.9rem;
  color: #aaaacc;
  margin-top: 10px;
}

/* ── Prediction cards ──────────────────────────────────── */
.pred-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
  animation: slideInUp 0.4s ease both;
  transition: border-color 0.3s, transform 0.2s;
}
.pred-card:hover {
  border-color: var(--clutch-orange);
  transform: translateY(-2px);
}
.pred-card.strong {
  border-color: rgba(255,184,0,0.4);
  background: linear-gradient(135deg, #111118, #1a1200);
}
.pred-pick {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2rem;
  letter-spacing: 0.05em;
  color: var(--clutch-orange);
  line-height: 1;
}
.pred-game {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 4px;
}
.conf-badge {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.2rem;
  letter-spacing: 0.05em;
}
.conf-strong { color: var(--clutch-gold); }
.conf-good   { color: var(--clutch-green); }
.conf-lean   { color: var(--clutch-blue); }

/* ── WON / LOST badges ─────────────────────────────────── */
.badge-won {
  display: inline-block;
  background: rgba(0,230,118,0.12);
  color: var(--clutch-green);
  border: 1px solid var(--clutch-green);
  border-radius: 6px;
  padding: 4px 14px;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  letter-spacing: 0.12em;
  animation: glowPulse 2s ease-in-out infinite;
}
.badge-lost {
  display: inline-block;
  background: rgba(255,23,68,0.1);
  color: var(--clutch-red);
  border: 1px solid var(--clutch-red);
  border-radius: 6px;
  padding: 4px 14px;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  letter-spacing: 0.12em;
  animation: redGlow 2s ease-in-out infinite;
}
.badge-pending {
  display: inline-block;
  background: rgba(0,176,255,0.08);
  color: var(--clutch-blue);
  border: 1px solid rgba(0,176,255,0.3);
  border-radius: 6px;
  padding: 4px 14px;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.1rem;
  letter-spacing: 0.12em;
}

/* ── Record display ────────────────────────────────────── */
.record-display {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 3.5rem;
  letter-spacing: 0.08em;
  text-align: center;
  line-height: 1;
  animation: fadeIn 0.6s ease;
}
.record-w { color: var(--clutch-green); }
.record-d { color: var(--text-muted); margin: 0 8px; }
.record-l { color: var(--clutch-red); }
.streak-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 4px;
  display: inline-block;
  margin-top: 4px;
}
.streak-w { background: rgba(0,230,118,0.15); color: var(--clutch-green); }
.streak-l { background: rgba(255,23,68,0.1);  color: var(--clutch-red); }

/* ── Live dot ──────────────────────────────────────────── */
.live-dot {
  display: inline-block;
  width: 10px; height: 10px;
  background: var(--clutch-red);
  border-radius: 50%;
  animation: livePulse 1.2s ease-in-out infinite;
  margin-right: 6px;
  vertical-align: middle;
}
.live-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--clutch-red);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  vertical-align: middle;
}

/* ── Countdown ─────────────────────────────────────────── */
.countdown-wrap {
  background: rgba(255,107,53,0.05);
  border: 1px solid rgba(255,107,53,0.2);
  border-radius: 10px;
  padding: 12px 20px;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin: 8px 0;
  animation: borderFlow 6s linear infinite;
}
.countdown-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--text-muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

/* ── Game slate card ───────────────────────────────────── */
.slate-card {
  background: var(--bg-surface);
  border-radius: 10px;
  padding: 14px 18px;
  margin: 8px 0;
  border-left: 3px solid var(--clutch-orange);
  animation: slideInLeft 0.3s ease both;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.slate-teams {
  font-family: 'Inter', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}
.slate-time {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--clutch-orange);
  letter-spacing: 0.05em;
}

/* ── Stats bar ─────────────────────────────────────────── */
.stat-bar-outer {
  background: rgba(255,255,255,0.06);
  border-radius: 4px;
  height: 6px;
  width: 100%;
  margin: 4px 0;
}
.stat-bar-inner {
  height: 6px;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--clutch-orange), var(--clutch-gold));
  transition: width 0.6s ease;
}

/* ── Section headers ───────────────────────────────────── */
.section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.6rem;
  letter-spacing: 0.1em;
  color: var(--clutch-orange);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  margin-bottom: 16px;
}

/* ── Score card ────────────────────────────────────────── */
.score-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 24px;
  margin-bottom: 12px;
  transition: border-color 0.3s;
}
.score-card:hover { border-color: rgba(255,107,53,0.4); }
.score-num {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.8rem;
  letter-spacing: 0.05em;
  line-height: 1;
}
.score-team {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* ── Metrics override ──────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Bebas Neue', sans-serif !important;
  font-size: 2rem !important;
  letter-spacing: 0.05em !important;
}

/* ── Tab styling ───────────────────────────────────────── */
[data-testid="stTabs"] button {
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.05em !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--clutch-orange) !important;
  border-bottom-color: var(--clutch-orange) !important;
}

/* ── Sidebar ───────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--bg-dark) !important;
}

/* ── Injury status badges ──────────────────────────────── */
.inj-out       { color: #FF1744; font-weight: 700; }
.inj-doubtful  { color: #FF9100; font-weight: 700; }
.inj-question  { color: #FFD600; font-weight: 600; }
.inj-probable  { color: #00E676; font-weight: 600; }

/* ── Data source pill ──────────────────────────────────── */
.data-pill {
  display: inline-block;
  background: rgba(0,176,255,0.1);
  color: var(--clutch-blue);
  border: 1px solid rgba(0,176,255,0.25);
  border-radius: 20px;
  padding: 2px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin: 2px;
  vertical-align: middle;
}

/* ── AI Analysis label ─────────────────────────────────── */
.ai-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--clutch-gold);
  letter-spacing: 0.15em;
  text-transform: uppercase;
  opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════
ESPN_BASE  = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
ESPN_CORE  = "https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba"
NBA_STATS  = "https://stats.nba.com/stats"
BDL_BASE   = "https://www.balldontlie.io/api/v1"   # free, no key
ODDS_API   = "https://api.the-odds-api.com/v4"

CONFIDENCE_THRESHOLD = 52.0
SEASON = "2025-26"
SEASON_BDL = "2025"

DEFAULT_TOTAL    = 228.5
DEFAULT_Q1_TOTAL = 57.0
DEFAULT_H1_TOTAL = 119.0

CAT_OFFSET = timedelta(hours=2)

HEADERS_ESPN = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}
HEADERS_NBA = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
}

STAR_IMPACT = {'OUT': 20, 'DOUBTFUL': 15, 'QUESTIONABLE': 8, 'PROBABLE': 3}
STATUS_FINAL   = ('STATUS_FINAL', 'Final', 'final', 'Completed', 'STATUS_COMPLETE')
UPCOMING_STATUSES = {'STATUS_SCHEDULED', 'Scheduled', 'scheduled', 'STATUS_DELAYED'}

# ── Default factor weights (overridden by self-learning DB values) ─
DEFAULT_WEIGHTS: Dict[str, float] = {
    "Home court Q1":      1.2,
    "Home Q1 scoring":    2.5,
    "Away Q1 scoring":    2.0,
    "Home starters":      3.0,
    "Away absences":      2.5,
    "Recent momentum":    1.5,
    "Home rest":          1.5,
    "Home ORTG":          1.8,
    "Away DRTG":          1.5,
    "Back-to-back":       2.0,
    "Home Q1 avg":        2.0,
    "Away Q1 avg":        2.0,
    "Combined Q1 pace":   1.5,
    "Combined health":    2.0,
    "Advanced pace":      2.0,
    "B2B sluggish start": 2.5,
}

BET_TYPE_ICONS = {
    "Q1 Spread":     "⚡",
    "Q1 Total OVER": "📈",
    "Moneyline":     "🎯",
    "Point Spread":  "📐",
    "Total — OVER":  "🔼",
    "Total — UNDER": "🔽",
    "1st Half Total":"⏱️",
}


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════

def to_cat(utc_str: str) -> str:
    try:
        dt = datetime.fromisoformat(utc_str.replace('Z', '+00:00'))
        return (dt + CAT_OFFSET).strftime('%d %b %Y · %H:%M CAT')
    except Exception:
        return utc_str or '—'

def to_cat_short(utc_str: str) -> str:
    try:
        dt = datetime.fromisoformat(utc_str.replace('Z', '+00:00'))
        return (dt + CAT_OFFSET).strftime('%d %b · %H:%M CAT')
    except Exception:
        return '—'

def utc_str_to_epoch(utc_str: str) -> Optional[int]:
    """Return Unix timestamp (ms) for use in JS countdown."""
    try:
        dt = datetime.fromisoformat(utc_str.replace('Z', '+00:00'))
        return int(dt.timestamp() * 1000)
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════
#  DATABASE LAYER
# ══════════════════════════════════════════════════════════════

@st.cache_resource
def get_db():
    conn = sqlite3.connect('clutch_nba.db', check_same_thread=False)
    conn.execute('''CREATE TABLE IF NOT EXISTS api_cache (
        cache_key TEXT PRIMARY KEY,
        data      TEXT,
        ts        REAL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS predictions_log (
        id          TEXT PRIMARY KEY,
        game_id     TEXT,
        game_label  TEXT,
        bet_type    TEXT,
        pick        TEXT,
        line        REAL,
        confidence  REAL,
        factors     TEXT,
        rationale   TEXT,
        created_at  TEXT,
        result      TEXT DEFAULT 'pending',
        final_score TEXT DEFAULT ''
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS win_loss_record (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT,
        total_won   INTEGER DEFAULT 0,
        total_lost  INTEGER DEFAULT 0,
        win_rate    REAL DEFAULT 0.0
    )''')
    # ── Self-learning tables ──────────────────────────────────
    conn.execute('''CREATE TABLE IF NOT EXISTS factor_weights (
        factor_name  TEXT PRIMARY KEY,
        weight       REAL DEFAULT 1.0,
        update_count INTEGER DEFAULT 0,
        last_updated TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS model_params (
        param_key TEXT PRIMARY KEY,
        value     REAL
    )''')
    conn.execute("INSERT OR IGNORE INTO model_params VALUES ('confidence_scalar', 1.8)")
    conn.execute("INSERT OR IGNORE INTO model_params VALUES ('min_confidence', 52.0)")
    conn.commit()
    return conn


def db_get(key: str, ttl: int = 300) -> Optional[Any]:
    try:
        row = get_db().execute('SELECT data, ts FROM api_cache WHERE cache_key=?', (key,)).fetchone()
        if row and (time.time() - row[1]) < ttl:
            return json.loads(row[0])
    except Exception:
        pass
    return None


def db_set(key: str, data: Any):
    try:
        conn = get_db()
        conn.execute('INSERT OR REPLACE INTO api_cache VALUES (?,?,?)',
                     (key, json.dumps(data, default=str), time.time()))
        conn.commit()
    except Exception:
        pass


def save_prediction(pred_dict: Dict, game_label: str):
    try:
        pid = hashlib.md5(
            f"{pred_dict['game_id']}{pred_dict['bet_type']}{pred_dict['pick']}".encode()
        ).hexdigest()[:12]
        conn = get_db()
        conn.execute('''INSERT OR IGNORE INTO predictions_log
            (id, game_id, game_label, bet_type, pick, line, confidence, factors, rationale, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)''', (
            pid, pred_dict['game_id'], game_label,
            pred_dict['bet_type'], pred_dict['pick'], pred_dict.get('line'),
            pred_dict['confidence'],
            json.dumps(pred_dict.get('factors', []), default=str),
            pred_dict.get('rationale', ''),
            datetime.now().isoformat()
        ))
        conn.commit()
    except Exception:
        pass


def get_record_stats() -> Dict:
    """Return W, L, pending, streak, win_rate from DB."""
    try:
        conn = sqlite3.connect('clutch_nba.db', check_same_thread=False)
        rows = conn.execute(
            "SELECT result, created_at FROM predictions_log ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        won = sum(1 for r in rows if r[0] == 'WON')
        lost = sum(1 for r in rows if r[0] == 'LOST')
        pending = sum(1 for r in rows if r[0] == 'pending')
        graded = [r[0] for r in rows if r[0] in ('WON', 'LOST')]
        # Calculate streak
        streak_char, streak_count = '', 0
        for g in graded:
            if streak_char == '':
                streak_char = g
                streak_count = 1
            elif g == streak_char:
                streak_count += 1
            else:
                break
        win_rate = (won / (won + lost) * 100) if (won + lost) > 0 else 0.0
        return {
            'won': won, 'lost': lost, 'pending': pending,
            'total_graded': won + lost,
            'win_rate': win_rate,
            'streak': f"{streak_char[0] if streak_char else '—'}{streak_count}" if streak_count else '—',
            'streak_type': streak_char,
        }
    except Exception:
        return {'won': 0, 'lost': 0, 'pending': 0, 'total_graded': 0,
                'win_rate': 0.0, 'streak': '—', 'streak_type': ''}


# ══════════════════════════════════════════════════════════════
#  SELF-LEARNING ENGINE — Weight adaptation & calibration
# ══════════════════════════════════════════════════════════════

def load_learned_weights() -> Dict[str, float]:
    """Load per-factor weights from DB, falling back to defaults."""
    try:
        rows = get_db().execute(
            "SELECT factor_name, weight FROM factor_weights"
        ).fetchall()
        learned = {r[0]: r[1] for r in rows}
        return {**DEFAULT_WEIGHTS, **learned}   # learned overrides defaults
    except Exception:
        return DEFAULT_WEIGHTS.copy()


def load_model_params() -> Dict[str, float]:
    """Load confidence scalar and min threshold from DB."""
    try:
        rows = get_db().execute(
            "SELECT param_key, value FROM model_params"
        ).fetchall()
        return dict(rows) if rows else {'confidence_scalar': 1.8, 'min_confidence': 52.0}
    except Exception:
        return {'confidence_scalar': 1.8, 'min_confidence': 52.0}


def _calibrate_model(conn) -> None:
    """
    Adjust confidence scalar so predicted confidence tracks actual win-rate.
    Called automatically after each grading cycle.
    """
    try:
        rows = conn.execute(
            "SELECT confidence, result FROM predictions_log "
            "WHERE result IN ('WON','LOST') ORDER BY created_at DESC LIMIT 60"
        ).fetchall()
        if len(rows) < 10:
            return

        avg_conf = float(np.mean([r[0] for r in rows]))
        win_rate = sum(1 for r in rows if r[1] == 'WON') / len(rows) * 100.0

        # Pull current scalar
        s_row = conn.execute(
            "SELECT value FROM model_params WHERE param_key='confidence_scalar'"
        ).fetchone()
        current_scalar = s_row[0] if s_row else 1.8

        # Calibration error: positive → we're over-confident
        cal_err = avg_conf - win_rate
        adj_scalar = current_scalar - cal_err * 0.003          # gentle nudge
        new_scalar = round(max(1.0, min(3.5, adj_scalar)), 4)
        conn.execute(
            "INSERT OR REPLACE INTO model_params VALUES ('confidence_scalar', ?)",
            (new_scalar,)
        )

        # Threshold: if winning consistently, allow more picks (lower threshold)
        t_row = conn.execute(
            "SELECT value FROM model_params WHERE param_key='min_confidence'"
        ).fetchone()
        current_thr = t_row[0] if t_row else 52.0
        thr_adj = (55.0 - win_rate) * 0.04                    # < 55% → raise bar
        new_thr = round(max(48.0, min(65.0, current_thr + thr_adj)), 2)
        conn.execute(
            "INSERT OR REPLACE INTO model_params VALUES ('min_confidence', ?)",
            (new_thr,)
        )
    except Exception:
        pass


def adapt_weights(factors_json: str, result: str) -> None:
    """
    EMA weight update after each graded prediction.

    Logic:
      WON  + factor score > 60  → factor was bullish and correct  → increase weight
      WON  + factor score < 40  → factor was bearish but we won   → decrease weight slightly
      LOST + factor score > 60  → factor was bullish but wrong    → decrease weight
      LOST + factor score < 40  → factor was bearish and correct  → increase weight slightly

    Weights are clamped to [0.3, 6.0] to prevent runaway values.
    """
    if result not in ('WON', 'LOST'):
        return
    try:
        factors = json.loads(factors_json or '[]')
        conn    = get_db()
        lr      = 0.07                          # learning rate per update

        for fac in factors:
            name  = fac.get('name', '')
            score = float(fac.get('score', 50))
            if not name:
                continue

            row = conn.execute(
                "SELECT weight, update_count FROM factor_weights WHERE factor_name=?",
                (name,)
            ).fetchone()
            cur_w = row[0] if row else DEFAULT_WEIGHTS.get(name, 1.5)
            n_upd = (row[1] if row else 0) + 1

            # Compute signal
            if result == 'WON':
                delta = lr * 0.4 if score > 60 else (-lr * 0.15 if score < 40 else 0.0)
            else:
                delta = -lr * 0.4 if score > 60 else (lr * 0.15 if score < 40 else 0.0)

            new_w = round(max(0.3, min(6.0, cur_w * (1 + delta))), 4)

            conn.execute(
                '''INSERT OR REPLACE INTO factor_weights
                   (factor_name, weight, update_count, last_updated)
                   VALUES (?, ?, ?, ?)''',
                (name, new_w, n_upd, datetime.now().isoformat())
            )

        _calibrate_model(conn)
        conn.commit()
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════
#  GRADING ENGINE
# ══════════════════════════════════════════════════════════════

def grade_pick(bet_type: str, pick: str, line,
               home_name: str, away_name: str, game: Dict) -> Optional[str]:
    hs    = int(game.get('home_score', 0) or 0)
    as_   = int(game.get('away_score', 0) or 0)
    total = hs + as_
    q1_h  = float(game.get('q1_home', 0) or 0)
    q1_a  = float(game.get('q1_away', 0) or 0)
    q2_h  = float(game.get('q2_home', 0) or 0)
    q2_a  = float(game.get('q2_away', 0) or 0)

    try:
        if bet_type == 'Moneyline':
            home_won    = hs > as_
            picked_home = home_name.lower() in pick.lower()
            correct     = home_won == picked_home

        elif 'Q1 Total' in bet_type or ('Total' in bet_type and 'Q1' in pick.upper()):
            if line is None or (q1_h + q1_a) == 0:
                return None
            picked_over = 'OVER' in pick.upper()
            correct     = (q1_h + q1_a > line) == picked_over

        elif '1st Half' in bet_type or '1H' in pick.upper():
            actual = q1_h + q2_h + q1_a + q2_a
            if line is None or actual == 0:
                return None
            picked_over = 'OVER' in pick.upper()
            correct     = (actual > line) == picked_over

        elif 'Total' in bet_type:
            if line is None or total == 0:
                return None
            picked_over = 'OVER' in pick.upper()
            correct     = (total > line) == picked_over

        elif 'Q1 Spread' in bet_type:
            if line is None or (q1_h + q1_a) == 0:
                return None
            picked_home_side = home_name.lower() in pick.lower()
            margin = (q1_h - q1_a) if picked_home_side else (q1_a - q1_h)
            nums   = re.findall(r'[-+]?\d+\.?\d*', pick.split('Q1')[-1])
            spread_val = float(nums[0]) if nums else 0.0
            correct = margin > abs(spread_val) if spread_val < 0 else margin > -abs(spread_val)

        elif 'Q1 Spread' in bet_type and 'win Q1' in pick:
            # "Team to win Q1 by ~N pts" → did they win Q1?
            home_won_q1 = q1_h > q1_a
            picked_home = home_name.lower() in pick.lower()
            correct = home_won_q1 == picked_home

        else:
            return None

        return 'WON' if correct else 'LOST'
    except Exception:
        return None


def grade_predictions() -> int:
    conn = get_db()
    pending = conn.execute(
        "SELECT id, game_id, game_label, bet_type, pick, line FROM predictions_log WHERE result = 'pending'"
    ).fetchall()
    if not pending:
        return 0

    updated = 0
    for pred_id, game_id, game_label, bet_type, pick, line in pending:
        parts = game_label.split(' @ ')
        if len(parts) != 2:
            # Try "vs" format
            parts = game_label.split(' vs ')
            if len(parts) != 2:
                continue
        away_name, home_name = parts[0].strip(), parts[1].strip()

        home_id_raw = ''
        if 'v' in game_id and not game_id.startswith('prop'):
            home_id_raw = game_id.split('v')[0]
        if not home_id_raw:
            continue

        games_list = fetch_team_schedule(home_id_raw)
        matched = next(
            (g for g in games_list
             if g.get('status') in STATUS_FINAL
             and (g.get('home_team', '').lower() == home_name.lower()
                  or home_name.lower() in g.get('home_team', '').lower())
             and (g.get('away_team', '').lower() == away_name.lower()
                  or away_name.lower() in g.get('away_team', '').lower())),
            None
        )
        if not matched:
            continue

        result = grade_pick(bet_type, pick, line, home_name, away_name, matched)
        if result:
            final_score = (
                f"{matched.get('away_score','?')}-{matched.get('home_score','?')}"
                f" | Q1: {int(matched.get('q1_away',0) or 0)}-{int(matched.get('q1_home',0) or 0)}"
            )
            conn.execute(
                "UPDATE predictions_log SET result = ?, final_score = ?, rationale = rationale || ? WHERE id = ?",
                (result, final_score, f" [Final: {final_score}]", pred_id)
            )
            # ── Self-learning: adapt weights from this outcome ──
            fac_row = conn.execute(
                "SELECT factors FROM predictions_log WHERE id=?", (pred_id,)
            ).fetchone()
            if fac_row and fac_row[0]:
                adapt_weights(fac_row[0], result)
            updated += 1

    if updated:
        conn.commit()
    return updated


# ══════════════════════════════════════════════════════════════
#  API FETCHERS
# ══════════════════════════════════════════════════════════════

def safe_get(url: str, headers: Dict, params: Dict = None, timeout: int = 12) -> Optional[Dict]:
    try:
        r = requests.get(url, headers=headers, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


@st.cache_data(ttl=120, show_spinner=False)
def fetch_upcoming_events() -> List[Dict]:
    found = []
    for delta in [0, 1, 2]:
        date_str = (datetime.utcnow() + timedelta(days=delta)).strftime('%Y%m%d')
        data = safe_get(f"{ESPN_BASE}/scoreboard", HEADERS_ESPN, params={'dates': date_str})
        if not data:
            continue
        for ev in data.get('events', []):
            comps = ev.get('competitions', [])
            if not comps:
                continue
            status_type = comps[0].get('status', {}).get('type', {})
            status_name = status_type.get('name', '')
            completed   = status_type.get('completed', False)
            if completed or status_name in STATUS_FINAL:
                continue
            if status_name in ('STATUS_IN_PROGRESS', 'STATUS_HALFTIME',
                               'STATUS_END_PERIOD', 'InProgress'):
                continue
            found.append(ev)
        if found:
            break
    found.sort(key=lambda e: e.get('date', ''))
    return found


@st.cache_data(ttl=60, show_spinner=False)
def fetch_scoreboard() -> Dict:
    return safe_get(f"{ESPN_BASE}/scoreboard", HEADERS_ESPN) or {}


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_team_stats(team_id: str) -> Dict:
    if not team_id:
        return {}
    key = f"tstats_{team_id}_{datetime.now().strftime('%Y%m%d')}"
    cached = db_get(key, ttl=3600)
    if cached:
        return cached
    data = safe_get(f"{ESPN_BASE}/teams/{team_id}/statistics", HEADERS_ESPN) or {}
    if data:
        db_set(key, data)
    return data


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_injuries() -> List[Dict]:
    key = f"injuries_{datetime.now().strftime('%Y%m%d%H')}"
    cached = db_get(key, ttl=1800)
    if cached:
        return cached
    injuries = []
    data = safe_get(f"{ESPN_BASE}/injuries", HEADERS_ESPN)
    if data:
        for team_entry in data.get('injuries', []):
            team_info = team_entry.get('team', {})
            for inj in team_entry.get('injuries', []):
                athlete = inj.get('athlete', {})
                injuries.append({
                    'team':        team_info.get('displayName', ''),
                    'team_abbr':   team_info.get('abbreviation', ''),
                    'team_id':     str(team_info.get('id', '')),
                    'player':      athlete.get('displayName', ''),
                    'player_id':   str(athlete.get('id', '')),
                    'position':    athlete.get('position', {}).get('abbreviation', ''),
                    'status':      inj.get('status', ''),
                    'description': inj.get('shortComment', '') or inj.get('longComment', ''),
                    'return_date': inj.get('returnDate', ''),
                })
    if injuries:
        db_set(key, injuries)
    return injuries


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_team_schedule(team_id: str) -> List[Dict]:
    if not team_id:
        return []
    key = f"sched_{team_id}_{datetime.now().strftime('%Y%m%d')}"
    cached = db_get(key, ttl=3600)
    if cached:
        return cached
    data = safe_get(f"{ESPN_BASE}/teams/{team_id}/schedule", HEADERS_ESPN)
    if not data:
        return []
    games = []
    for ev in data.get('events', []):
        comps = ev.get('competitions', [])
        if not comps:
            continue
        comp = comps[0]
        competitors = comp.get('competitors', [])
        if len(competitors) < 2:
            continue
        home = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
        away = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])

        def _score(c):
            s = c.get('score')
            if isinstance(s, dict):
                return int(s.get('value', 0) or 0)
            try:
                return int(s or 0)
            except (TypeError, ValueError):
                return 0

        def _q_score(comp_obj, period, team_type):
            for ln in comp_obj.get('linescores', []):
                period_num = ln.get('period', ln.get('sequence'))
                if str(period_num) == str(period):
                    competitors_ln = comp_obj.get('competitors', [])
                    for c in competitors_ln:
                        if c.get('homeAway') == team_type:
                            for ls in c.get('linescores', []):
                                if str(ls.get('period', ls.get('sequence'))) == str(period):
                                    try:
                                        return float(ls.get('value', 0) or 0)
                                    except Exception:
                                        return 0.0
            return 0.0

        # Quarter scores via linescores on competitor
        def _q(competitor_obj, period):
            for ls in competitor_obj.get('linescores', []):
                p = ls.get('period', ls.get('sequence'))
                if str(p) == str(period):
                    try:
                        return float(ls.get('value', 0) or 0)
                    except Exception:
                        return 0.0
            return 0.0

        status_name = comp.get('status', {}).get('type', {}).get('name', '')
        home_won_flag = any(r.get('winner') for r in home.get('records', []) if isinstance(r, dict))

        games.append({
            'game_id':    ev.get('id', ''),
            'date':       ev.get('date', ''),
            'home_team':  home.get('team', {}).get('displayName', ''),
            'away_team':  away.get('team', {}).get('displayName', ''),
            'home_score': _score(home),
            'away_score': _score(away),
            'home_winner': home.get('winner', False),
            'q1_home':    _q(home, 1),
            'q1_away':    _q(away, 1),
            'q2_home':    _q(home, 2),
            'q2_away':    _q(away, 2),
            'q3_home':    _q(home, 3),
            'q3_away':    _q(away, 3),
            'status':     status_name,
        })
    db_set(key, games)
    return games


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nba_advanced_stats() -> Dict[str, Dict]:
    """
    Fetch league-wide advanced team stats from NBA Stats API.
    Returns dict keyed by team abbreviation.
    ORTG, DRTG, PACE, NET_RATING, eFG%, TS% etc.
    """
    key = f"adv_stats_{datetime.now().strftime('%Y%m%d')}"
    cached = db_get(key, ttl=86400)
    if cached:
        return cached

    data = safe_get(
        f"{NBA_STATS}/leaguedashteamstats",
        HEADERS_NBA,
        params={
            'Season': SEASON,
            'SeasonType': 'Regular Season',
            'PerMode': 'PerGame',
            'MeasureType': 'Advanced',
            'PaceAdjust': 'N',
            'LeagueID': '00',
        },
        timeout=20
    )
    result = {}
    if data:
        try:
            hdrs = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            for row in rows:
                d = dict(zip(hdrs, row))
                abbr = d.get('TEAM_ABBREVIATION', '')
                if abbr:
                    result[abbr] = {
                        'team_name': d.get('TEAM_NAME', ''),
                        'ortg':  float(d.get('OFF_RATING', 110) or 110),
                        'drtg':  float(d.get('DEF_RATING', 110) or 110),
                        'net':   float(d.get('NET_RATING', 0) or 0),
                        'pace':  float(d.get('PACE', 99) or 99),
                        'efg':   float(d.get('EFG_PCT', 0.5) or 0.5),
                        'ts':    float(d.get('TS_PCT', 0.55) or 0.55),
                        'oreb':  float(d.get('OREB_PCT', 0.25) or 0.25),
                        'dreb':  float(d.get('DREB_PCT', 0.75) or 0.75),
                        'ast':   float(d.get('AST_PCT', 0.6) or 0.6),
                        'tov':   float(d.get('TM_TOV_PCT', 0.13) or 0.13),
                    }
        except Exception:
            pass
    if result:
        db_set(key, result)
    return result


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nba_base_stats() -> Dict[str, Dict]:
    """Fetch base scoring stats (PTS, REB, AST per game) from NBA Stats."""
    key = f"base_stats_{datetime.now().strftime('%Y%m%d')}"
    cached = db_get(key, ttl=86400)
    if cached:
        return cached
    data = safe_get(
        f"{NBA_STATS}/leaguedashteamstats",
        HEADERS_NBA,
        params={
            'Season': SEASON,
            'SeasonType': 'Regular Season',
            'PerMode': 'PerGame',
            'MeasureType': 'Base',
            'LeagueID': '00',
        },
        timeout=20
    )
    result = {}
    if data:
        try:
            hdrs = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            for row in rows:
                d = dict(zip(hdrs, row))
                abbr = d.get('TEAM_ABBREVIATION', '')
                if abbr:
                    result[abbr] = {
                        'pts':   float(d.get('PTS', 110) or 110),
                        'reb':   float(d.get('REB', 43) or 43),
                        'ast':   float(d.get('AST', 24) or 24),
                        'fgpct': float(d.get('FG_PCT', 0.46) or 0.46),
                        'fg3pct':float(d.get('FG3_PCT', 0.35) or 0.35),
                        'blk':   float(d.get('BLK', 4.5) or 4.5),
                        'stl':   float(d.get('STL', 7) or 7),
                        'tov':   float(d.get('TOV', 13) or 13),
                        'w_pct': float(d.get('W_PCT', 0.5) or 0.5),
                        'gp':    int(d.get('GP', 1) or 1),
                    }
        except Exception:
            pass
    if result:
        db_set(key, result)
    return result


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_player_gamelog(player_id: str) -> List[Dict]:
    if not player_id:
        return []
    key = f"gamelog_{player_id}_{datetime.now().strftime('%Y%m%d')}"
    cached = db_get(key, ttl=7200)
    if cached:
        return cached
    data = safe_get(
        f"{NBA_STATS}/playergamelog",
        HEADERS_NBA,
        params={'PlayerID': player_id, 'Season': SEASON,
                'SeasonType': 'Regular Season', 'LastNGames': 50},
        timeout=15
    )
    if not data:
        return []
    try:
        hdrs = data['resultSets'][0]['headers']
        rows = data['resultSets'][0]['rowSet']
        games = [dict(zip(hdrs, row)) for row in rows]
        db_set(key, games)
        return games
    except Exception:
        return []


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_all_teams() -> List[Dict]:
    data = safe_get(f"{ESPN_BASE}/teams", HEADERS_ESPN)
    if not data:
        return []
    teams = []
    for sport in data.get('sports', []):
        for league in sport.get('leagues', []):
            for t_wrap in league.get('teams', []):
                t = t_wrap.get('team', {})
                teams.append({
                    'id':   str(t.get('id', '')),
                    'name': t.get('displayName', ''),
                    'abbr': t.get('abbreviation', ''),
                    'logo': t.get('logos', [{}])[0].get('href', '') if t.get('logos') else '',
                })
    return teams


@st.cache_data(ttl=600, show_spinner=False)
def fetch_game_summary(event_id: str) -> Dict:
    return safe_get(f"{ESPN_BASE}/summary", HEADERS_ESPN, params={'event': event_id}) or {}


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_odds(api_key: str) -> List[Dict]:
    if not api_key:
        return []
    data = safe_get(
        f"{ODDS_API}/sports/basketball_nba/odds",
        {},
        params={'apiKey': api_key, 'regions': 'us,eu', 'markets': 'spreads,totals',
                'oddsFormat': 'decimal'}
    )
    return data or []


def extract_espn_odds(comp: Dict) -> Dict:
    result = {}
    odds_list = comp.get('odds', [])
    if not odds_list:
        return result
    od = odds_list[0]
    ou = od.get('overUnder')
    if ou:
        try:
            val = float(ou)
            if val > 150:
                result['total'] = val
        except (TypeError, ValueError):
            pass
    sp_raw = od.get('spread')
    if sp_raw:
        try:
            result['spread'] = abs(float(sp_raw))
        except (TypeError, ValueError):
            pass
    if 'spread' not in result:
        details = od.get('details', '')
        if isinstance(details, str):
            m = re.search(r'[-+]?\d+\.?\d*$', details.strip())
            if m:
                try:
                    result['spread'] = abs(float(m.group()))
                except ValueError:
                    pass
    return result


# ══════════════════════════════════════════════════════════════
#  FACTOR ENGINE
# ══════════════════════════════════════════════════════════════

@dataclass
class Factor:
    name:        str
    weight:      float
    score:       float
    description: str

    @property
    def weighted_score(self) -> float:
        return self.weight * self.score


@dataclass
class Prediction:
    game_id:    str
    game_label: str
    bet_type:   str
    pick:       str
    line:       Optional[float]
    confidence: float
    factors:    List[Factor]
    rationale:  str
    value_edge: float
    tip_off:    str = ""
    tip_off_utc: str = ""  # raw UTC for countdown

    def to_dict(self) -> Dict:
        return {
            'game_id':    self.game_id,
            'game_label': self.game_label,
            'bet_type':   self.bet_type,
            'pick':       self.pick,
            'line':       self.line,
            'confidence': round(self.confidence, 2),
            'factors':    [{'name': f.name, 'score': round(f.score, 1),
                            'weight': f.weight, 'description': f.description}
                           for f in self.factors],
            'rationale':  self.rationale,
            'value_edge': round(self.value_edge, 2),
        }


class Factors:

    @staticmethod
    def health(team_id: str, injury_map: Dict) -> Tuple[float, str]:
        inj = injury_map.get(str(team_id), [])
        if not inj:
            return 100.0, "Full strength"
        penalty, flagged = 0.0, []
        for i in inj:
            s = i.get('status', '').upper()
            for kw, p in STAR_IMPACT.items():
                if kw in s:
                    penalty += p
                    flagged.append(f"{i.get('player','?')} ({i.get('position','')}) {s}")
                    break
        return max(0.0, 100.0 - penalty), ' | '.join(flagged) if flagged else "Full strength"

    @staticmethod
    def form(games: List[Dict], team_name: str, n: int = 10) -> Tuple[float, str]:
        completed = [g for g in games if g.get('status') in STATUS_FINAL]
        last = completed[-n:]
        if not last:
            return 50.0, "No game data"
        weighted_wins, total_wt, margins, wins_count = 0.0, 0.0, [], 0
        for i, g in enumerate(last):
            wt = 1.0 + (i / len(last)) * 1.5
            is_home = g.get('home_team', '') == team_name
            hs, as_ = g.get('home_score', 0), g.get('away_score', 0)
            won = (is_home and hs > as_) or (not is_home and as_ > hs)
            margin = (hs - as_) if is_home else (as_ - hs)
            if won:
                weighted_wins += wt
                wins_count += 1
            total_wt += wt
            margins.append(margin)
        pct = (weighted_wins / total_wt) * 100 if total_wt else 50
        avg_m = np.mean(margins) if margins else 0
        return pct, f"Last {len(last)}: {wins_count}W–{len(last)-wins_count}L | avg margin {avg_m:+.1f}"

    @staticmethod
    def home_court(is_home: bool) -> Tuple[float, str]:
        return (65.0, "Home court advantage (+3 pts)") if is_home else (38.0, "Road team disadvantage")

    @staticmethod
    def offense(team_stats: Dict) -> Tuple[float, str]:
        try:
            for cat in team_stats.get('splits', {}).get('categories', []):
                for s in cat.get('stats', []):
                    if s.get('name') in ('avgPoints', 'pointsPerGame', 'avgPointsFor'):
                        pts = float(s.get('value', 0))
                        if pts > 60:
                            return min(100, max(0, (pts - 100) / 30 * 100)), f"Avg {pts:.1f} pts/game"
        except Exception:
            pass
        return 50.0, "Offense stats unavailable"

    @staticmethod
    def offense_from_log(games: List[Dict], team_name: str) -> Tuple[float, str]:
        scores = [float(g.get('home_score' if g.get('home_team', '') == team_name else 'away_score', 0))
                  for g in games if g.get('status') in STATUS_FINAL
                  and (g.get('home_score') or g.get('away_score', 0)) > 60]
        if len(scores) < 5:
            return 50.0, "Insufficient scoring data"
        avg = np.mean(scores[-20:])
        return min(100, max(0, (avg - 100) / 30 * 100)), f"Avg {avg:.1f} pts/game (n={min(20,len(scores))})"

    @staticmethod
    def defense(team_stats: Dict) -> Tuple[float, str]:
        try:
            for cat in team_stats.get('splits', {}).get('categories', []):
                for s in cat.get('stats', []):
                    if s.get('name') in ('avgPointsAllowed', 'avgOppPoints', 'pointsAllowedPerGame'):
                        pts = float(s.get('value', 0))
                        if pts > 60:
                            return min(100, max(0, (130 - pts) / 30 * 100)), f"Allows {pts:.1f} pts/game"
        except Exception:
            pass
        return 50.0, "Defense stats unavailable"

    @staticmethod
    def defense_from_log(games: List[Dict], team_name: str) -> Tuple[float, str]:
        allowed = [float(g.get('away_score' if g.get('home_team', '') == team_name else 'home_score', 0))
                   for g in games if g.get('status') in STATUS_FINAL
                   and (g.get('away_score') or g.get('home_score', 0)) > 60]
        if len(allowed) < 5:
            return 50.0, "Insufficient defense data"
        avg = np.mean(allowed[-20:])
        return min(100, max(0, (130 - avg) / 30 * 100)), f"Allows {avg:.1f} pts/game"

    @staticmethod
    def best_offense(team_stats, games, team_name):
        sc, d = Factors.offense(team_stats)
        return (sc, d) if sc != 50.0 else Factors.offense_from_log(games, team_name)

    @staticmethod
    def best_defense(team_stats, games, team_name):
        sc, d = Factors.defense(team_stats)
        return (sc, d) if sc != 50.0 else Factors.defense_from_log(games, team_name)

    @staticmethod
    def advanced_ortg(adv: Dict, team_abbr: str) -> Tuple[float, str]:
        """Offensive rating from NBA Stats advanced data. League avg ≈ 113."""
        d = adv.get(team_abbr, {})
        ortg = d.get('ortg', 113.0)
        score = min(100, max(0, (ortg - 100) / 20 * 100))
        return score, f"ORTG: {ortg:.1f} (league avg ~113)"

    @staticmethod
    def advanced_drtg(adv: Dict, team_abbr: str) -> Tuple[float, str]:
        """Defensive rating — lower is better. 100 = elite, 120 = poor."""
        d = adv.get(team_abbr, {})
        drtg = d.get('drtg', 113.0)
        score = min(100, max(0, (125 - drtg) / 25 * 100))
        return score, f"DRTG: {drtg:.1f} (lower = better defense)"

    @staticmethod
    def advanced_pace(adv: Dict, team_abbr: str) -> Tuple[float, str]:
        d = adv.get(team_abbr, {})
        pace = d.get('pace', 99.0)
        score = min(100, max(0, (pace - 90) / 20 * 100))
        return score, f"Pace: {pace:.1f} poss/game"

    @staticmethod
    def advanced_net(adv: Dict, team_abbr: str) -> Tuple[float, str]:
        d = adv.get(team_abbr, {})
        net = d.get('net', 0.0)
        score = min(100, max(0, 50 + net * 4))
        return score, f"Net rating: {net:+.1f}"

    @staticmethod
    def win_pct(base: Dict, team_abbr: str) -> Tuple[float, str]:
        d = base.get(team_abbr, {})
        wpct = d.get('w_pct', 0.5)
        gp   = d.get('gp', 1)
        return wpct * 100, f"Season record: {wpct:.1%} over {gp} games"

    @staticmethod
    def efg(adv: Dict, team_abbr: str) -> Tuple[float, str]:
        d = adv.get(team_abbr, {})
        efg = d.get('efg', 0.5)
        score = min(100, max(0, (efg - 0.40) / 0.20 * 100))
        return score, f"eFG%: {efg:.1%}"

    @staticmethod
    def rest(team_games: List[Dict]) -> Tuple[float, str]:
        completed = [g for g in team_games
                     if g.get('date') and g.get('status') in STATUS_FINAL]
        if not completed:
            return 50.0, "Rest data unavailable"
        try:
            last_dt = datetime.fromisoformat(completed[-1]['date'].replace('Z', '+00:00'))
            days = (datetime.now().astimezone() - last_dt).days
            if days == 0:
                return 25.0, "Back-to-back — fatigue risk"
            if days == 1:
                return 55.0, "1 day rest"
            if days >= 3:
                return 80.0, f"{days}d rest — fresh legs"
            return 65.0, f"{days}d rest"
        except Exception:
            return 50.0, "Rest unavailable"

    @staticmethod
    def q1_avg(games: List[Dict], team_name: str) -> Tuple[float, str]:
        q1s = [float(g.get('q1_home' if g.get('home_team','') == team_name else 'q1_away', 0))
               for g in games if g.get('status') in STATUS_FINAL
               and (g.get('q1_home') or g.get('q1_away', 0)) > 0]
        if len(q1s) < 5:
            return 50.0, "Insufficient Q1 data"
        avg, std = np.mean(q1s), np.std(q1s)
        score = min(100, max(0, (avg - 22) / 14 * 100))
        return score, f"Q1 avg: {avg:.1f} pts (σ={std:.1f}, n={len(q1s)})"

    @staticmethod
    def ats_coverage(games: List[Dict], team_name: str, spread: Optional[float]) -> Tuple[float, str]:
        if spread is None:
            return 50.0, "No spread data"
        margins = []
        for g in games:
            if g.get('status') not in STATUS_FINAL:
                continue
            is_home = g.get('home_team', '') == team_name
            hs, as_ = g.get('home_score', 0), g.get('away_score', 0)
            margins.append((hs - as_) if is_home else (as_ - hs))
        if not margins:
            return 50.0, "No margin data"
        covers = sum(1 for m in margins if m > spread)
        return covers / len(margins) * 100, f"Covers {spread:+.1f} in {covers}/{len(margins)} games"

    @staticmethod
    def pace(team_stats: Dict) -> Tuple[float, str]:
        try:
            for cat in team_stats.get('splits', {}).get('categories', []):
                for s in cat.get('stats', []):
                    if s.get('name') in ('pace', 'avgPace', 'possessionsPerGame'):
                        val = float(s.get('value', 0))
                        return min(100, max(0, (val - 90) / 20 * 100)), f"Pace: {val:.1f}"
        except Exception:
            pass
        return 50.0, "Pace data unavailable"

    @staticmethod
    def h2h(home_games: List[Dict], away_games: List[Dict],
            home_name: str, away_name: str) -> Tuple[float, str]:
        h2h_games = [g for g in home_games + away_games
                     if g.get('home_team', '') in (home_name, away_name)
                     and g.get('away_team', '') in (home_name, away_name)
                     and g.get('status') in STATUS_FINAL]
        if not h2h_games:
            return 50.0, "No H2H data this season"
        home_wins = sum(1 for g in h2h_games
                        if g.get('home_team') == home_name and g.get('home_winner'))
        return home_wins / len(h2h_games) * 100, f"H2H: {home_name} {home_wins}/{len(h2h_games)} at home"

    @staticmethod
    def b2b_check(games: List[Dict]) -> Tuple[bool, str]:
        completed = sorted([g for g in games if g.get('date')], key=lambda x: x.get('date', ''))
        if len(completed) < 2:
            return False, "Not on back-to-back"
        try:
            last_dt = datetime.fromisoformat(completed[-1]['date'].replace('Z', '+00:00'))
            days_since = (datetime.now().astimezone() - last_dt).days
            return days_since == 0, f"{'ON' if days_since == 0 else 'NOT ON'} B2B"
        except Exception:
            return False, "B2B check failed"

    @staticmethod
    def player_prop(gamelog: List[Dict], stat_key: str, line: float,
                    stat_display: str) -> Tuple[float, str, float]:
        vals = []
        for g in gamelog:
            v = g.get(stat_key)
            if v is not None:
                try:
                    vals.append(float(v))
                except Exception:
                    pass
        if len(vals) < 10:
            return 50.0, f"Insufficient data for {stat_display}", 0.0
        avg     = np.mean(vals)
        recent  = np.mean(vals[:10])
        over_ct = sum(1 for v in vals if v > line)
        over_pct = over_ct / len(vals) * 100
        return (over_pct,
                f"Avg {avg:.1f} | Recent {recent:.1f} | Over {line} in {over_ct}/{len(vals)} games",
                avg)


# ══════════════════════════════════════════════════════════════
#  PREDICTION ENGINE
# ══════════════════════════════════════════════════════════════

class Engine:
    def __init__(self, injury_map: Dict, adv_stats: Dict = None, base_stats: Dict = None,
                 learned_weights: Dict = None, model_params: Dict = None):
        self.inj    = injury_map
        self.adv    = adv_stats or {}
        self.base   = base_stats or {}
        self.w      = learned_weights or DEFAULT_WEIGHTS.copy()
        self.params = model_params or {'confidence_scalar': 1.8, 'min_confidence': 52.0}

    def W(self, name: str) -> float:
        """Return the learned weight for a factor, falling back to default."""
        return self.w.get(name, DEFAULT_WEIGHTS.get(name, 1.5))

    @staticmethod
    def _confidence(factors: List[Factor], scalar: float = 1.8) -> float:
        tw = sum(f.weight for f in factors)
        if tw == 0:
            return 0.0
        wav = sum(f.weighted_score for f in factors) / tw
        conf = 50.0 + (wav - 50.0) * scalar
        return min(99.0, max(0.0, conf))

    @staticmethod
    def _top_reasons(factors: List[Factor], n: int = 3) -> str:
        top = sorted(factors, key=lambda f: f.weighted_score, reverse=True)[:n]
        return " · ".join(f"{f.name}: {f.description}" for f in top)

    def _get_abbr(self, name: str) -> str:
        """Best-effort match team name to abbreviation for advanced stats."""
        name_lower = name.lower()
        for abbr, d in self.adv.items():
            if name_lower in d.get('team_name', '').lower():
                return abbr
        # Fallback: match last word
        last = name.split()[-1].lower()
        for abbr, d in self.adv.items():
            if last in d.get('team_name', '').lower():
                return abbr
        return ''

    def q1_spread(self, home: Dict, away: Dict, hg: List, ag: List,
                  q1_line: Optional[float]) -> Optional[Prediction]:
        f = []
        h_abbr = self._get_abbr(home['name'])
        a_abbr = self._get_abbr(away['name'])

        hca_s, hca_d = Factors.home_court(True)
        f.append(Factor("Home court Q1",   self.W("Home court Q1"),   hca_s + 5, hca_d))

        hq_s, hq_d = Factors.q1_avg(hg, home['name'])
        aq_s, aq_d = Factors.q1_avg(ag, away['name'])
        f.append(Factor("Home Q1 scoring", self.W("Home Q1 scoring"), hq_s, hq_d))
        f.append(Factor("Away Q1 scoring", self.W("Away Q1 scoring"), 100 - aq_s, f"Opp: {aq_d}"))

        hi_s, hi_d = Factors.health(home['id'], self.inj)
        ai_s, ai_d = Factors.health(away['id'], self.inj)
        f.append(Factor("Home starters",   self.W("Home starters"),   hi_s, hi_d))
        f.append(Factor("Away absences",   self.W("Away absences"),   100 - ai_s, f"Opp: {ai_d}"))

        hf_s, hf_d = Factors.form(hg, home['name'], 5)
        f.append(Factor("Recent momentum", self.W("Recent momentum"), hf_s, hf_d))

        hr_s, hr_d = Factors.rest(hg)
        f.append(Factor("Home rest",       self.W("Home rest"),       hr_s, hr_d))

        if h_abbr:
            ho_s, ho_d = Factors.advanced_ortg(self.adv, h_abbr)
            f.append(Factor("Home ORTG",   self.W("Home ORTG"),       ho_s, ho_d))
        if a_abbr:
            ad_s, ad_d = Factors.advanced_drtg(self.adv, a_abbr)
            f.append(Factor("Away DRTG",   self.W("Away DRTG"),       100 - ad_s, ad_d))

        b2b_h, _ = Factors.b2b_check(hg)
        if b2b_h:
            f.append(Factor("Back-to-back", self.W("Back-to-back"),   20.0, "Q1 pace hurt on B2B"))

        scalar = self.params.get('confidence_scalar', 1.8)
        conf = self._confidence(f, scalar)
        home_q1_edge = (hq_s * self.W("Home Q1 scoring") + hi_s * self.W("Home starters") + hca_s * self.W("Home court Q1")) / (self.W("Home Q1 scoring") + self.W("Home starters") + self.W("Home court Q1"))
        away_q1_edge = (aq_s * self.W("Away Q1 scoring") + ai_s * self.W("Away absences")) / (self.W("Away Q1 scoring") + self.W("Away absences"))

        if home_q1_edge >= away_q1_edge:
            pick_team = home['name']
            margin_est = round(abs(home_q1_edge - away_q1_edge) / 5, 1)
        else:
            pick_team = away['name']
            margin_est = round(abs(home_q1_edge - away_q1_edge) / 5, 1)

        pick = f"{pick_team} to win Q1 by ~{margin_est:.0f}pts"

        return Prediction(
            game_id=f"{home['id']}v{away['id']}",
            game_label=f"{away['name']} @ {home['name']}",
            bet_type="Q1 Spread", pick=pick, line=q1_line,
            confidence=conf, factors=f,
            rationale=self._top_reasons(f),
            value_edge=conf - 50.0
        )

    def q1_total(self, home: Dict, away: Dict, hg: List, ag: List,
                 q1_line: Optional[float]) -> Optional[Prediction]:
        f = []
        h_abbr = self._get_abbr(home['name'])
        a_abbr = self._get_abbr(away['name'])

        hq_s, hq_d = Factors.q1_avg(hg, home['name'])
        aq_s, aq_d = Factors.q1_avg(ag, away['name'])
        f.append(Factor("Home Q1 avg",      self.W("Home Q1 avg"),      hq_s, hq_d))
        f.append(Factor("Away Q1 avg",      self.W("Away Q1 avg"),      aq_s, aq_d))
        f.append(Factor("Combined Q1 pace", self.W("Combined Q1 pace"), (hq_s + aq_s) / 2, "Both teams Q1 tendency"))

        hi_s, _ = Factors.health(home['id'], self.inj)
        ai_s, _ = Factors.health(away['id'], self.inj)
        f.append(Factor("Combined health",  self.W("Combined health"),  (hi_s + ai_s) / 2, "H+A"))

        if h_abbr and a_abbr:
            h_pace, _ = Factors.advanced_pace(self.adv, h_abbr)
            a_pace, _ = Factors.advanced_pace(self.adv, a_abbr)
            f.append(Factor("Advanced pace", self.W("Advanced pace"), (h_pace + a_pace) / 2,
                            f"H:{self.adv.get(h_abbr,{}).get('pace',99):.1f} A:{self.adv.get(a_abbr,{}).get('pace',99):.1f}"))

        b2b_h, _ = Factors.b2b_check(hg)
        b2b_a, _ = Factors.b2b_check(ag)
        if b2b_h or b2b_a:
            f.append(Factor("B2B sluggish start", self.W("B2B sluggish start"), 20.0, "B2B → Q1 typically 2-4 pts below avg"))

        scalar = self.params.get('confidence_scalar', 1.8)
        conf = self._confidence(f, scalar)
        pick = f"Q1 OVER {q1_line:.1f}" if q1_line else "Q1 OVER"

        return Prediction(
            game_id=f"{home['id']}v{away['id']}",
            game_label=f"{away['name']} @ {home['name']}",
            bet_type="Q1 Total OVER", pick=pick, line=q1_line,
            confidence=conf, factors=f,
            rationale=self._top_reasons(f),
            value_edge=conf - 50.0
        )

    def analyze_game(self, home: Dict, away: Dict,
                     home_stats: Dict, away_stats: Dict,
                     home_games: List, away_games: List,
                     odds_markets: Optional[Dict] = None) -> List[Prediction]:
        spread_line = odds_markets.get('spread') if odds_markets else None
        total_line  = odds_markets.get('total')  if odds_markets else None
        q1_line     = round(spread_line * 0.25, 1) if spread_line else None
        q1_total    = round(total_line  * 0.25, 1) if total_line  else None

        preds = []
        for fn, kw in [
            (self.q1_spread, {'q1_line': q1_line}),
            (self.q1_total,  {'q1_line': q1_total}),
        ]:
            try:
                p = fn(home, away, home_games, away_games, **kw)
                if p:
                    preds.append(p)
            except Exception:
                pass
        return preds


# ══════════════════════════════════════════════════════════════
#  COUNTDOWN COMPONENT
# ══════════════════════════════════════════════════════════════

def render_countdown(tip_off_utc: str, game_label: str):
    """Render a live JS countdown to tip-off inside a Streamlit component."""
    epoch_ms = utc_str_to_epoch(tip_off_utc)
    if not epoch_ms:
        return
    # Unique ID per game
    uid = hashlib.md5(game_label.encode()).hexdigest()[:8]
    html = f"""
<div style="display:flex; align-items:center; gap:10px; margin:6px 0;">
  <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem;
               color:#888; letter-spacing:0.12em; text-transform:uppercase;">
    TIP-OFF IN
  </span>
  <span id="cd_{uid}" style="font-family:'JetBrains Mono',monospace; font-size:1.5rem;
              font-weight:700; color:#FF6B35; letter-spacing:0.05em;
              animation: none;">00:00:00</span>
  <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem;
               color:#555; letter-spacing:0.1em;">CAT</span>
</div>
<script>
(function() {{
  var tip = {epoch_ms};
  var el  = document.getElementById('cd_{uid}');
  function fmt(n) {{ return n < 10 ? '0' + n : '' + n; }}
  function tick() {{
    var now  = Date.now();
    var diff = tip - now;
    if (diff <= 0) {{
      el.textContent = '🏀 LIVE';
      el.style.color = '#FF1744';
      return;
    }}
    var h = Math.floor(diff / 3600000);
    var m = Math.floor((diff % 3600000) / 60000);
    var s = Math.floor((diff % 60000) / 1000);
    el.textContent = fmt(h) + ':' + fmt(m) + ':' + fmt(s);
    if (diff < 1800000) {{ el.style.color = '#FFB800'; }}
    if (diff < 300000)  {{ el.style.color = '#FF1744'; }}
    setTimeout(tick, 1000);
  }}
  tick();
}})();
</script>
"""
    components.html(html, height=46)


# ══════════════════════════════════════════════════════════════
#  PREDICTION CARD RENDERER
# ══════════════════════════════════════════════════════════════

def conf_tier(c: float) -> str:
    if c >= 75: return "🔥 STRONG"
    if c >= 65: return "✅ SOLID"
    if c >= 57: return "⚡ LEAN"
    return "⚪ MARGINAL"

def conf_class(c: float) -> str:
    if c >= 75: return "conf-strong"
    if c >= 65: return "conf-good"
    return "conf-lean"


def render_pred(pred: Prediction):
    icon  = BET_TYPE_ICONS.get(pred.bet_type, "🎯")
    tier  = conf_tier(pred.confidence)
    cls   = conf_class(pred.confidence)
    is_strong = pred.confidence >= 75

    card_class = "pred-card strong" if is_strong else "pred-card"

    col1, col2, col3 = st.columns([4, 1.5, 1])
    with col1:
        st.markdown(f"""
<div class="{card_class}">
  <div class="pred-game">{icon} {pred.bet_type} &nbsp;·&nbsp; {pred.game_label}</div>
  <div class="pred-pick">{pred.pick}</div>
  <div style="font-family:'Inter',sans-serif;font-size:0.82rem;color:#aaa;margin-top:6px;">
    {pred.rationale[:140]}{"…" if len(pred.rationale) > 140 else ""}
  </div>
  <div style="margin-top:8px;">
    <span class="data-pill">ESPN</span>
    <span class="data-pill">NBA Stats</span>
    {"<span class='data-pill'>Advanced</span>" if is_strong else ""}
    {f'<span class="ai-label" style="margin-left:6px;">🕐 {pred.tip_off}</span>' if pred.tip_off else ""}
  </div>
</div>
""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
<div style="text-align:center; padding:12px 0;">
  <div class="conf-badge {cls}">{pred.confidence:.1f}%</div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
              color:#888;letter-spacing:0.1em;margin-top:4px;">{tier}</div>
  <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#666;margin-top:4px;">
    +{pred.value_edge:.1f}% edge
  </div>
</div>
""", unsafe_allow_html=True)

    with col3:
        with st.popover("📊 Analysis"):
            st.markdown(f"**{pred.bet_type}**")
            st.caption(pred.game_label)
            if pred.tip_off:
                st.caption(f"🕐 {pred.tip_off}")
            if pred.tip_off_utc:
                render_countdown(pred.tip_off_utc, pred.game_label)
            st.divider()
            for fac in sorted(pred.factors, key=lambda f: f.weighted_score, reverse=True):
                bar_val = min(1.0, max(0.0, fac.score / 100))
                st.progress(bar_val, text=f"**{fac.name}** {fac.score:.0f}/100 — {fac.description}")

    if pred.tip_off_utc:
        render_countdown(pred.tip_off_utc, pred.game_label + "_main")

    st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  RESULTS RENDERER — Full transparency W/L
# ══════════════════════════════════════════════════════════════

def render_results_tab(tab):
    with tab:
        # Title
        st.markdown('<div class="section-title">RESULTS · WIN/LOSS RECORD</div>',
                    unsafe_allow_html=True)

        col_refresh, _ = st.columns([1, 5])
        with col_refresh:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()

        with st.spinner("Grading pending predictions…"):
            newly_graded = grade_predictions()

        if newly_graded > 0:
            st.toast(f"✅ {newly_graded} prediction(s) graded!", icon="🏀")
            st.rerun()

        # Fresh DB read
        try:
            conn = sqlite3.connect('clutch_nba.db', check_same_thread=False)
            all_rows = conn.execute(
                '''SELECT game_label, bet_type, pick, line, confidence, result,
                          rationale, created_at, final_score
                   FROM predictions_log ORDER BY created_at DESC'''
            ).fetchall()
            conn.close()
            cols = ['game_label','bet_type','pick','line','confidence',
                    'result','rationale','created_at','final_score']
            df_all = pd.DataFrame(all_rows, columns=cols) if all_rows else pd.DataFrame(columns=cols)
        except Exception as e:
            st.error(f"Database error: {e}")
            return

        if df_all.empty:
            st.info("No predictions logged yet. Run the Predictions tab to generate picks.")
            return

        won_df     = df_all[df_all['result'] == 'WON']
        lost_df    = df_all[df_all['result'] == 'LOST']
        pending_df = df_all[df_all['result'] == 'pending']
        graded_df  = df_all[df_all['result'].isin(['WON','LOST'])]
        total_graded = len(graded_df)
        win_rate = len(won_df) / total_graded * 100 if total_graded else 0.0

        # Calculate streak
        results_list = df_all[df_all['result'].isin(['WON','LOST'])]['result'].tolist()
        streak_char, streak_count = '', 0
        for r in results_list:
            if not streak_char:
                streak_char, streak_count = r, 1
            elif r == streak_char:
                streak_count += 1
            else:
                break
        streak_label = f"{streak_char[0] if streak_char else '?'}{streak_count}" if streak_count else '—'
        streak_css   = 'streak-w' if streak_char == 'WON' else ('streak-l' if streak_char == 'LOST' else '')

        # ── Big Record ──────────────────────────────────────────
        st.markdown(f"""
<div style="background:#111118;border:1px solid rgba(255,107,53,0.15);
            border-radius:14px;padding:28px;text-align:center;margin-bottom:20px;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#666;
              letter-spacing:0.2em;text-transform:uppercase;margin-bottom:8px;">
    All-Time Record
  </div>
  <div class="record-display">
    <span class="record-w">{len(won_df)}</span>
    <span class="record-d">–</span>
    <span class="record-l">{len(lost_df)}</span>
  </div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;
              color:{'#00E676' if win_rate >= 55 else '#FFB800' if win_rate >= 50 else '#FF6B35'};
              letter-spacing:0.1em;margin-top:6px;">
    {win_rate:.1f}% WIN RATE
  </div>
  <div style="margin-top:10px;">
    <span class="streak-badge {streak_css}">STREAK: {streak_label}</span>
    &nbsp;
    <span class="badge-pending" style="font-size:0.8rem;">{len(pending_df)} PENDING</span>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Metrics row ─────────────────────────────────────────
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("✅ Won",      len(won_df))
        m2.metric("❌ Lost",     len(lost_df))
        m3.metric("⏳ Pending",  len(pending_df))
        m4.metric("📊 Graded",   total_graded)
        m5.metric("🎯 Win Rate", f"{win_rate:.1f}%" if total_graded else "—")

        st.divider()

        # ── By bet type breakdown ───────────────────────────────
        if total_graded > 0:
            st.markdown('<div class="section-title" style="font-size:1.1rem;">BY BET TYPE</div>',
                        unsafe_allow_html=True)
            bt_stats = []
            for bt in sorted(graded_df['bet_type'].unique()):
                bt_df = graded_df[graded_df['bet_type'] == bt]
                w  = len(bt_df[bt_df['result'] == 'WON'])
                l  = len(bt_df[bt_df['result'] == 'LOST'])
                wr = w / len(bt_df) * 100
                bt_stats.append({'Bet Type': bt, '✅ Won': w, '❌ Lost': l,
                                  'Total': len(bt_df), 'Win %': f"{wr:.0f}%"})
            st.dataframe(pd.DataFrame(bt_stats), hide_index=True, use_container_width=True)
            st.divider()

        # ── Recent form (last 10 graded) ────────────────────────
        if total_graded >= 3:
            last10 = results_list[:10]
            st.markdown("**Recent Form (newest → oldest)**")
            dots = ""
            for r in last10:
                if r == 'WON':
                    dots += '<span class="badge-won" style="font-size:0.75rem;padding:2px 8px;margin:2px;">W</span>'
                else:
                    dots += '<span class="badge-lost" style="font-size:0.75rem;padding:2px 8px;margin:2px;">L</span>'
            st.markdown(dots, unsafe_allow_html=True)
            st.divider()

        # ── Won list ────────────────────────────────────────────
        st.markdown(f"### ✅ Correct ({len(won_df)})")
        if won_df.empty:
            st.info("No graded wins yet — results appear after games finish.")
        else:
            for _, r in won_df.iterrows():
                score_str = str(r.get('final_score','') or '').strip()
                st.markdown(f"""
<div style="background:rgba(0,230,118,0.05);border:1px solid rgba(0,230,118,0.2);
            border-radius:10px;padding:14px 18px;margin:8px 0;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div>
      <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;
                  color:#F0F0F5;">{r['bet_type']} · {r['game_label']}</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                  color:#FF6B35;letter-spacing:0.05em;">{r['pick']}</div>
      <div style="font-size:0.78rem;color:#666;margin-top:2px;">
        {str(r.get('rationale',''))[:110]}…
        {f'<br><span style="color:#4ade80;font-size:0.75rem;">📊 {score_str}</span>' if score_str else ''}
      </div>
    </div>
    <div style="text-align:right;flex-shrink:0;padding-left:16px;">
      <span class="badge-won">WON</span>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                  color:#00E676;margin-top:4px;">{float(r['confidence']):.1f}%</div>
      <div style="font-size:0.7rem;color:#666;">
        {str(r.get('created_at',''))[:16].replace('T',' ')}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.divider()

        # ── Lost list ───────────────────────────────────────────
        st.markdown(f"### ❌ Missed ({len(lost_df)})")
        if lost_df.empty:
            st.info("No graded losses yet.")
        else:
            for _, r in lost_df.iterrows():
                score_str = str(r.get('final_score','') or '').strip()
                st.markdown(f"""
<div style="background:rgba(255,23,68,0.04);border:1px solid rgba(255,23,68,0.18);
            border-radius:10px;padding:14px 18px;margin:8px 0;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;">
    <div>
      <div style="font-family:'Inter',sans-serif;font-weight:700;font-size:0.95rem;
                  color:#F0F0F5;">{r['bet_type']} · {r['game_label']}</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                  color:#888;letter-spacing:0.05em;">{r['pick']}</div>
      <div style="font-size:0.78rem;color:#666;margin-top:2px;">
        {str(r.get('rationale',''))[:110]}…
        {f'<br><span style="color:#f87171;font-size:0.75rem;">📊 {score_str}</span>' if score_str else ''}
      </div>
    </div>
    <div style="text-align:right;flex-shrink:0;padding-left:16px;">
      <span class="badge-lost">MISSED</span>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;
                  color:#FF6B35;margin-top:4px;">{float(r['confidence']):.1f}%</div>
      <div style="font-size:0.7rem;color:#666;">
        {str(r.get('created_at',''))[:16].replace('T',' ')}
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Pending ─────────────────────────────────────────────
        if not pending_df.empty:
            st.divider()
            with st.expander(f"⏳ Pending — {len(pending_df)} awaiting results"):
                st.caption("Auto-grades when games finish.")
                pend_data = []
                for _, r in pending_df.iterrows():
                    pend_data.append({
                        'Game': r['game_label'],
                        'Bet Type': r['bet_type'],
                        'Pick': r['pick'],
                        'Conf': f"{float(r['confidence']):.1f}%",
                        'Line': r['line'] if r['line'] else '—',
                        'Logged': str(r.get('created_at',''))[:16].replace('T',' '),
                    })
                st.dataframe(pd.DataFrame(pend_data), hide_index=True, use_container_width=True)


# ══════════════════════════════════════════════════════════════
#  LEARNING TAB — Transparency into self-modification
# ══════════════════════════════════════════════════════════════

def render_learning_tab(tab):
    with tab:
        st.markdown('<div class="section-title">🧠 SELF-LEARNING MODEL</div>',
                    unsafe_allow_html=True)
        st.markdown("""
<div style="background:#111118;border:1px solid rgba(255,184,0,0.2);border-radius:12px;
            padding:16px 20px;margin-bottom:20px;font-family:'Inter',sans-serif;font-size:0.85rem;color:#aaa;">
  <b style="color:#FFB800;">How it works:</b> Every time a prediction is graded (WON or LOST),
  the engine performs an EMA weight update on every factor that contributed to that prediction.
  Factors that were bullish and correct get stronger; factors that were bullish but wrong get weaker.
  The confidence scalar is also calibrated so predicted confidence tracks actual win-rate.
  All changes persist in SQLite and take effect on the next prediction run.
</div>
""", unsafe_allow_html=True)

        # ── Model params ───────────────────────────────────────
        params = load_model_params()
        scalar = params.get('confidence_scalar', 1.8)
        thr    = params.get('min_confidence', 52.0)

        c1, c2, c3 = st.columns(3)
        c1.metric("Confidence Scalar", f"{scalar:.4f}",
                  delta=f"{scalar - 1.8:+.4f} vs default",
                  help="Amplifies/dampens confidence spread. Auto-calibrated to track actual win-rate.")
        c2.metric("Min Confidence Threshold", f"{thr:.2f}%",
                  delta=f"{thr - 52.0:+.2f}% vs default",
                  help="Picks below this threshold are suppressed. Raised when win-rate is low.")

        # ── Win-rate gauge ─────────────────────────────────────
        rec = get_record_stats()
        c3.metric("Live Win Rate", f"{rec['win_rate']:.1f}%",
                  delta=f"{rec['total_graded']} graded",
                  help="Current actual win rate used as calibration target.")

        st.divider()

        # ── Factor weights table ───────────────────────────────
        st.markdown("#### Factor Weights — Learned vs Default")
        try:
            rows = get_db().execute(
                "SELECT factor_name, weight, update_count, last_updated FROM factor_weights ORDER BY weight DESC"
            ).fetchall()
        except Exception:
            rows = []

        all_factors = list(DEFAULT_WEIGHTS.keys())
        learned_map = {r[0]: (r[1], r[2], r[3]) for r in rows}

        table_data = []
        for name in all_factors:
            default_w = DEFAULT_WEIGHTS[name]
            if name in learned_map:
                lw, n_upd, last = learned_map[name]
                delta_pct = (lw - default_w) / default_w * 100
                status = "📈 Stronger" if lw > default_w * 1.05 else ("📉 Weaker" if lw < default_w * 0.95 else "≈ Stable")
            else:
                lw, n_upd, last, delta_pct, status = default_w, 0, "—", 0.0, "⚪ Unchanged"
            table_data.append({
                'Factor':         name,
                'Default':        f"{default_w:.2f}",
                'Learned':        f"{lw:.4f}",
                'Change':         f"{delta_pct:+.1f}%",
                'Updates':        n_upd,
                'Status':         status,
                'Last Updated':   str(last or '—')[:16].replace('T', ' '),
            })

        if table_data:
            df_w = pd.DataFrame(table_data)

            def _color_change(v):
                try:
                    n = float(v.replace('%', ''))
                    if n > 5:   return 'color: #00E676'
                    if n < -5:  return 'color: #FF6B35'
                    return 'color: #888'
                except Exception:
                    return ''

            st.dataframe(
                df_w.style.map(_color_change, subset=['Change']),
                hide_index=True, use_container_width=True
            )
        else:
            st.info("No predictions graded yet — weights will appear here after the first graded result.")

        st.divider()

        # ── Learning history chart ─────────────────────────────
        st.markdown("#### Confidence Calibration Over Time")
        try:
            hist_rows = get_db().execute(
                """SELECT confidence, result, created_at FROM predictions_log
                   WHERE result IN ('WON','LOST') ORDER BY created_at ASC LIMIT 100"""
            ).fetchall()
            if len(hist_rows) >= 3:
                cal_df = pd.DataFrame(hist_rows, columns=['confidence', 'result', 'ts'])
                cal_df['correct'] = (cal_df['result'] == 'WON').astype(int) * 100
                cal_df['rolling_wr'] = cal_df['correct'].rolling(window=5, min_periods=1).mean()
                cal_df['rolling_conf'] = cal_df['confidence'].rolling(window=5, min_periods=1).mean()
                cal_df['game_no'] = range(1, len(cal_df) + 1)

                chart_df = cal_df[['game_no', 'rolling_conf', 'rolling_wr']].rename(columns={
                    'rolling_conf': 'Predicted Confidence %',
                    'rolling_wr':   'Actual Win Rate %',
                }).set_index('game_no')
                st.line_chart(chart_df, use_container_width=True)
                st.caption("Rolling 5-game window. Tighter gap = better calibration.")
            else:
                st.info("Chart appears after 3+ graded predictions.")
        except Exception as e:
            st.caption(f"Chart unavailable: {e}")

        st.divider()

        # ── Manual reset ───────────────────────────────────────
        with st.expander("⚠️ Reset learned weights to defaults"):
            st.warning("This wipes all learned weights and resets model params. Use only if the model is misbehaving.")
            if st.button("🔄 Reset All Learned Weights", type="primary"):
                try:
                    conn = get_db()
                    conn.execute("DELETE FROM factor_weights")
                    conn.execute("INSERT OR REPLACE INTO model_params VALUES ('confidence_scalar', 1.8)")
                    conn.execute("INSERT OR REPLACE INTO model_params VALUES ('min_confidence', 52.0)")
                    conn.commit()
                    st.success("✅ Weights reset to defaults. Reload the page to see changes.")
                except Exception as e:
                    st.error(f"Reset failed: {e}")


# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════

def main():
    # Auto-refresh
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=60_000, key="clutch_autorefresh")
    except ImportError:
        pass

    # ── Sidebar ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        odds_key = st.text_input("The Odds API Key", type="password",
                                  placeholder="optional — free at the-odds-api.com")
        if not odds_key:
            try:
                odds_key = st.secrets.get("ODDS_API_KEY", "")
            except Exception:
                pass

        st.divider()
        rec = get_record_stats()
        st.markdown(f"""
<div style="text-align:center;">
  <div style="font-family:'Bebas Neue',sans-serif;font-size:0.8rem;
              letter-spacing:0.15em;color:#666;">RECORD</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;letter-spacing:0.05em;">
    <span style="color:#00E676;">{rec['won']}</span>
    <span style="color:#444;">–</span>
    <span style="color:#FF1744;">{rec['lost']}</span>
  </div>
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#888;">
    {rec['win_rate']:.1f}% · Streak: {rec['streak']}
  </div>
</div>
""", unsafe_allow_html=True)
        st.divider()
        st.caption(f"🕐 {datetime.now().strftime('%H:%M:%S')} · {SEASON}")
        st.caption("💡 Add `ODDS_API_KEY` in Streamlit Secrets")

    # ── Hero header ───────────────────────────────────────────
    rec = get_record_stats()
    st.markdown(f"""
<div class="clutch-hero">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
    <div>
      <div class="clutch-title">CLUTCH</div>
      <div class="clutch-sub">NBA · Intelligence · System</div>
      <div class="clutch-tagline">
        Advanced AI predictions — 10+ data sources · Live injury data · Full transparency
      </div>
    </div>
    <div style="text-align:right;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:0.75rem;
                  letter-spacing:0.2em;color:#555;margin-bottom:4px;">ALL-TIME</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:2.8rem;
                  letter-spacing:0.05em;line-height:1;">
        <span style="color:#00E676;">{rec['won']}</span>
        <span style="color:#333;">–</span>
        <span style="color:#FF1744;">{rec['lost']}</span>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.8rem;
                  color:{'#00E676' if rec['win_rate'] >= 55 else '#FFB800'};">
        {rec['win_rate']:.1f}% win rate
      </div>
    </div>
  </div>
  <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">
    <span class="data-pill">ESPN Scoreboard</span>
    <span class="data-pill">NBA Advanced Stats</span>
    <span class="data-pill">ORTG · DRTG · PACE</span>
    <span class="data-pill">eFG% · TS%</span>
    <span class="data-pill">Injury Reports</span>
    <span class="data-pill">H2H Records</span>
    <span class="data-pill">B2B Fatigue</span>
    <span class="data-pill">Live Odds</span>
    <span class="data-pill" style="background:rgba(255,184,0,0.12);color:#FFB800;border-color:rgba(255,184,0,0.3);">🧠 Self-Learning</span>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────
    with st.spinner("Syncing live data…"):
        scoreboard      = fetch_scoreboard()
        upcoming_events = fetch_upcoming_events()
        injuries        = fetch_injuries()
        adv_stats       = fetch_nba_advanced_stats()
        base_stats      = fetch_nba_base_stats()
        odds_data       = fetch_odds(odds_key) if odds_key else []

    games = scoreboard.get('events', [])

    inj_map: Dict[str, List[Dict]] = {}
    for inj in injuries:
        tid = inj.get('team_id', '')
        if tid:
            inj_map.setdefault(tid, []).append(inj)

    odds_map: Dict[str, Dict] = {}
    for od in odds_data:
        home_key = od.get('home_team', '').lower()
        entry = {}
        for bm in od.get('bookmakers', [])[:2]:
            for mkt in bm.get('markets', []):
                key = mkt.get('key', '')
                if key == 'spreads':
                    for out in mkt.get('outcomes', []):
                        if od.get('home_team','').lower() in out.get('name','').lower():
                            entry['spread'] = abs(float(out.get('point', 0)))
                elif key == 'totals':
                    for out in mkt.get('outcomes', [])[:1]:
                        entry['total'] = float(out.get('point', DEFAULT_TOTAL))
        if entry:
            odds_map[home_key] = entry

    # ── Tabs ──────────────────────────────────────────────────
    tab_preds, tab_live, tab_injuries, tab_teams, tab_history, tab_results, tab_learn = st.tabs([
        "🎯 Predictions", "🟢 Live", "🏥 Injuries", "📊 Teams", "📖 Log", "🏆 Results", "🧠 Learning"
    ])

    engine = Engine(inj_map, adv_stats, base_stats,
                    learned_weights=load_learned_weights(),
                    model_params=load_model_params())

    # ══════════════════════════════════════════════════════════
    #  TAB 1 — PREDICTIONS
    # ══════════════════════════════════════════════════════════
    with tab_preds:
        st.markdown('<div class="section-title">TODAY\'S PICKS</div>', unsafe_allow_html=True)

        if not upcoming_events:
            st.info("No upcoming games in the next 48 hours, or ESPN data is loading.")
            st.caption("Could be an off-day, All-Star break, or end of season.")
        else:
            # Animated game slate
            cat_now = datetime.utcnow() + CAT_OFFSET
            with st.expander(f"📅 {len(upcoming_events)} game(s) on the slate", expanded=True):
                for ev in upcoming_events:
                    comps = ev.get('competitions', [])
                    if not comps:
                        continue
                    cptrs = comps[0].get('competitors', [])
                    if len(cptrs) < 2:
                        continue
                    home_c = next((c for c in cptrs if c.get('homeAway') == 'home'), cptrs[0])
                    away_c = next((c for c in cptrs if c.get('homeAway') == 'away'), cptrs[1])
                    h_name = home_c.get('team', {}).get('displayName', 'Home')
                    a_name = away_c.get('team', {}).get('displayName', 'Away')
                    tip_utc = ev.get('date', '')
                    tip_cat = to_cat(tip_utc)

                    st.markdown(f"""
<div class="slate-card">
  <div>
    <div class="slate-teams">🏀 {a_name} <span style="color:#555">@</span> {h_name}</div>
    <div class="slate-time">🕐 {tip_cat}</div>
  </div>
</div>
""", unsafe_allow_html=True)
                    render_countdown(tip_utc, f"{a_name}@{h_name}")

            # Generate predictions
            all_preds: List[Prediction] = []
            prog = st.progress(0, "Analysing matchups…")

            for idx, event in enumerate(upcoming_events):
                prog.progress((idx + 1) / len(upcoming_events),
                              f"Game {idx+1}/{len(upcoming_events)}…")
                comps = event.get('competitions', [])
                if not comps:
                    continue
                comp = comps[0]
                competitors = comp.get('competitors', [])
                if len(competitors) < 2:
                    continue

                home_c = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
                away_c = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])

                home = {'id': str(home_c.get('team', {}).get('id', '')),
                        'name': home_c.get('team', {}).get('displayName', 'Home')}
                away = {'id': str(away_c.get('team', {}).get('id', '')),
                        'name': away_c.get('team', {}).get('displayName', 'Away')}

                tip_utc = event.get('date', '')
                tip_off_cat = to_cat_short(tip_utc)

                home_stats = fetch_team_stats(home['id'])
                away_stats = fetch_team_stats(away['id'])
                home_games = fetch_team_schedule(home['id'])
                away_games = fetch_team_schedule(away['id'])

                espn_lines  = extract_espn_odds(comp)
                matched_odds = {}
                for key_frag, od in odds_map.items():
                    if key_frag in home['name'].lower() or home['name'].lower().split()[-1] in key_frag:
                        matched_odds = od
                        break

                final_odds = {**matched_odds, **espn_lines}
                if not final_odds.get('total'):
                    final_odds['total'] = DEFAULT_TOTAL

                preds = engine.analyze_game(home, away, home_stats, away_stats,
                                             home_games, away_games, final_odds or None)
                for p in preds:
                    p.tip_off     = tip_off_cat
                    p.tip_off_utc = tip_utc
                    if p.bet_type in ["Q1 Spread", "Q1 Total OVER"]:
                        all_preds.append(p)
                        save_prediction(p.to_dict(), p.game_label)

            prog.empty()
            all_preds.sort(key=lambda x: x.confidence, reverse=True)

            if not all_preds:
                st.info("No predictions generated — ESPN data may still be loading.")
            else:
                strong = [p for p in all_preds if p.confidence >= 75]
                good   = [p for p in all_preds if 65 <= p.confidence < 75]
                lean   = [p for p in all_preds if p.confidence < 65]

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Games Analysed",   len(upcoming_events))
                m2.metric("🔥 Strong",        len(strong))
                m3.metric("✅ Solid",          len(good))
                m4.metric("⚡ Lean",           len(lean))

                st.markdown("""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#666;
            letter-spacing:0.08em;margin:10px 0;">
  🔥 STRONG ≥75% · ✅ SOLID 65–74% · ⚡ LEAN &lt;65% · sorted by confidence
</div>
""", unsafe_allow_html=True)

                st.divider()
                for pred in all_preds:
                    render_pred(pred)

    # ══════════════════════════════════════════════════════════
    #  TAB 2 — LIVE SCORES
    # ══════════════════════════════════════════════════════════
    with tab_live:
        st.markdown(f'<div class="section-title">LIVE · {datetime.now().strftime("%d %b %Y")}</div>',
                    unsafe_allow_html=True)

        if not games:
            st.info("No games today, or scoreboard loading…")
        else:
            for event in games:
                comps = event.get('competitions', [])
                if not comps:
                    continue
                comp = comps[0]
                competitors = comp.get('competitors', [])
                if len(competitors) < 2:
                    continue

                home_c = next((c for c in competitors if c.get('homeAway') == 'home'), competitors[0])
                away_c = next((c for c in competitors if c.get('homeAway') == 'away'), competitors[1])

                home_name = home_c.get('team', {}).get('displayName', 'Home')
                away_name = away_c.get('team', {}).get('displayName', 'Away')

                def _score(c):
                    s = c.get('score')
                    if isinstance(s, dict): return s.get('displayValue', '—')
                    return str(s) if s is not None else '—'

                hs = _score(home_c)
                as_ = _score(away_c)
                status = comp.get('status', {}).get('type', {}).get('description', 'Scheduled')
                game_utc = event.get('date', '')
                is_live  = comp.get('status', {}).get('type', {}).get('state', '') == 'in'

                live_html = '<span class="live-dot"></span><span class="live-label">LIVE</span>' if is_live else ''

                espn_od = comp.get('odds', [{}])
                odds_str = ''
                if espn_od and espn_od[0]:
                    od = espn_od[0]
                    if od.get('details'):
                        odds_str += f"Spread: <b>{od['details']}</b>"
                    if od.get('overUnder'):
                        odds_str += f"  ·  O/U: <b>{od['overUnder']}</b>"

                st.markdown(f"""
<div class="score-card">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
    <div style="flex:1;min-width:120px;">
      <div class="score-team">{away_name}</div>
      <div class="score-num" style="color:#F0F0F5;">{as_}</div>
    </div>
    <div style="text-align:center;padding:0 8px;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;
                  color:#444;letter-spacing:0.1em;">VS</div>
      <div style="margin-top:4px;">{live_html}</div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;
                  color:#666;margin-top:4px;">{status}</div>
    </div>
    <div style="flex:1;min-width:120px;text-align:right;">
      <div class="score-team">{home_name}</div>
      <div class="score-num" style="color:#FF6B35;">{hs}</div>
    </div>
  </div>
  {"<div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#666;margin-top:8px;'>" + odds_str + "</div>" if odds_str else ""}
  {"" if is_live else '<div style="margin-top:6px;">'}
  {"" if is_live else f'</div>'}
</div>
""", unsafe_allow_html=True)

                if not is_live and game_utc:
                    render_countdown(game_utc, f"live_{home_name}")

    # ══════════════════════════════════════════════════════════
    #  TAB 3 — INJURIES
    # ══════════════════════════════════════════════════════════
    with tab_injuries:
        st.markdown('<div class="section-title">INJURY REPORT</div>', unsafe_allow_html=True)

        if not injuries:
            st.info("Injury data loading or unavailable from ESPN.")
        else:
            STATUS_ICONS = {
                'OUT': ('🔴', 'inj-out'),
                'DOUBTFUL': ('🟠', 'inj-doubtful'),
                'QUESTIONABLE': ('🟡', 'inj-question'),
                'PROBABLE': ('🟢', 'inj-probable'),
                'DAY-TO-DAY': ('🟡', 'inj-question'),
            }
            teams_inj: Dict[str, List] = {}
            for inj in injuries:
                teams_inj.setdefault(inj.get('team', 'Unknown'), []).append(inj)

            sev_filter = st.multiselect(
                "Status filter",
                ["OUT","DOUBTFUL","QUESTIONABLE","PROBABLE","DAY-TO-DAY"],
                default=["OUT","DOUBTFUL","QUESTIONABLE"]
            )

            for team_name in sorted(teams_inj.keys()):
                inj_list = [i for i in teams_inj[team_name]
                            if any(kw in i.get('status','').upper() for kw in sev_filter)]
                if not inj_list:
                    continue
                with st.expander(f"🏀 {team_name}  ({len(inj_list)})"):
                    for inj in inj_list:
                        s  = inj.get('status', '').upper()
                        ic, css = next(((v,c) for k,(v,c) in STATUS_ICONS.items() if k in s), ('⚪',''))
                        pos = f"[{inj.get('position','')}]" if inj.get('position') else ""
                        st.markdown(f"{ic} **{inj.get('player','?')}** {pos} — "
                                    f"<span class='{css}'>{s}</span>", unsafe_allow_html=True)
                        if inj.get('description'):
                            st.caption(f"  {inj['description']}")
                        if inj.get('return_date'):
                            st.caption(f"  Expected return: {inj['return_date']}")

    # ══════════════════════════════════════════════════════════
    #  TAB 4 — TEAM ANALYSIS
    # ══════════════════════════════════════════════════════════
    with tab_teams:
        st.markdown('<div class="section-title">TEAM DEEP DIVE</div>', unsafe_allow_html=True)
        all_teams = fetch_all_teams()
        if not all_teams:
            st.warning("Teams data loading…")
        else:
            name_to_id = {t['name']: t['id'] for t in all_teams}
            team_abbrs = {t['name']: t.get('abbr','') for t in all_teams}
            sel = st.selectbox("Select team", sorted(name_to_id.keys()))
            if sel:
                tid  = name_to_id[sel]
                abbr = team_abbrs.get(sel, '')
                with st.spinner(f"Loading {sel} data…"):
                    t_stats = fetch_team_stats(tid)
                    t_games = fetch_team_schedule(tid)
                    t_inj   = [i for i in injuries if i.get('team') == sel]
                    t_adv   = adv_stats.get(abbr, {})
                    t_base  = base_stats.get(abbr, {})

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### Last 10 Games")
                    completed = [g for g in t_games if g.get('status') in STATUS_FINAL]
                    last10 = completed[-10:]
                    if last10:
                        rows = []
                        for g in reversed(last10):
                            is_h = g.get('home_team', '') == sel
                            hs, as_ = g.get('home_score', 0), g.get('away_score', 0)
                            won = (is_h and hs > as_) or (not is_h and as_ > hs)
                            margin = (hs - as_) if is_h else (as_ - hs)
                            opp = g.get('away_team' if is_h else 'home_team', '?')
                            rows.append({
                                'Result':   '✅' if won else '❌',
                                'Opponent': opp[:18],
                                'Score':    f"{hs}–{as_}",
                                'Margin':   f"{margin:+d}",
                                'Q1':       f"{g.get('q1_home' if is_h else 'q1_away', 0):.0f}",
                            })
                        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
                    else:
                        st.info("No completed games found.")

                    # Advanced stats
                    if t_adv:
                        st.markdown("#### Advanced Metrics")
                        adv_rows = [
                            {'Metric': 'Offensive Rating',  'Value': f"{t_adv.get('ortg',0):.1f}"},
                            {'Metric': 'Defensive Rating',  'Value': f"{t_adv.get('drtg',0):.1f}"},
                            {'Metric': 'Net Rating',        'Value': f"{t_adv.get('net',0):+.1f}"},
                            {'Metric': 'Pace',              'Value': f"{t_adv.get('pace',0):.1f}"},
                            {'Metric': 'eFG%',              'Value': f"{t_adv.get('efg',0):.1%}"},
                            {'Metric': 'True Shooting%',    'Value': f"{t_adv.get('ts',0):.1%}"},
                        ]
                        st.dataframe(pd.DataFrame(adv_rows), hide_index=True, use_container_width=True)

                with col_b:
                    st.markdown("#### Health Status")
                    if t_inj:
                        for inj in t_inj:
                            s = inj.get('status', '').upper()
                            ic = '🔴' if 'OUT' in s else ('🟠' if 'DOUBT' in s else '🟡')
                            st.markdown(f"{ic} **{inj.get('player','?')}** — {s}")
                            if inj.get('description'):
                                st.caption(f"  {inj['description']}")
                    else:
                        st.success("✅ Full squad available")

                    st.markdown("#### Season Averages")
                    if t_base:
                        base_rows = [
                            {'Stat': 'Points/Game',   'Value': f"{t_base.get('pts',0):.1f}"},
                            {'Stat': 'Rebounds/Game', 'Value': f"{t_base.get('reb',0):.1f}"},
                            {'Stat': 'Assists/Game',  'Value': f"{t_base.get('ast',0):.1f}"},
                            {'Stat': 'FG%',           'Value': f"{t_base.get('fgpct',0):.1%}"},
                            {'Stat': '3P%',           'Value': f"{t_base.get('fg3pct',0):.1%}"},
                            {'Stat': 'Win%',          'Value': f"{t_base.get('w_pct',0):.1%}"},
                        ]
                        st.dataframe(pd.DataFrame(base_rows), hide_index=True, use_container_width=True)
                    else:
                        stat_rows = []
                        for cat in t_stats.get('splits', {}).get('categories', []):
                            for s in cat.get('stats', []):
                                if s.get('name', '').startswith('avg'):
                                    try:
                                        stat_rows.append({'Stat': s.get('displayName', s.get('name','')),
                                                          'Value': f"{float(s.get('value',0)):.1f}"})
                                    except Exception:
                                        pass
                        if stat_rows:
                            st.dataframe(pd.DataFrame(stat_rows[:18]),
                                         hide_index=True, use_container_width=True)
                        else:
                            off_s, off_d = Factors.offense_from_log(t_games, sel)
                            def_s, def_d = Factors.defense_from_log(t_games, sel)
                            form_s, form_d = Factors.form(t_games, sel, 10)
                            st.dataframe(pd.DataFrame([
                                {'Stat': 'Offense (pts/game)', 'Value': off_d},
                                {'Stat': 'Defense (opp pts/game)', 'Value': def_d},
                                {'Stat': 'Last 10 form', 'Value': form_d},
                            ]), hide_index=True, use_container_width=True)

                # Q1 chart
                st.markdown("#### Q1 Scoring — Last 20 Games")
                q1_vals = []
                for g in completed[-20:]:
                    is_h = g.get('home_team', '') == sel
                    v = g.get('q1_home' if is_h else 'q1_away', 0)
                    if v and v > 0:
                        q1_vals.append({'Game': g.get('date', '')[:10], 'Q1 Score': float(v)})
                if q1_vals:
                    st.line_chart(pd.DataFrame(q1_vals).set_index('Game')['Q1 Score'],
                                  use_container_width=True)

    # ══════════════════════════════════════════════════════════
    #  TAB 5 — LOG
    # ══════════════════════════════════════════════════════════
    with tab_history:
        st.markdown('<div class="section-title">PREDICTION LOG</div>', unsafe_allow_html=True)
        try:
            conn = get_db()
            rows = conn.execute(
                '''SELECT game_label, bet_type, pick, confidence, result, created_at
                   FROM predictions_log ORDER BY created_at DESC LIMIT 300'''
            ).fetchall()
            if rows:
                df = pd.DataFrame(rows, columns=['Game','Bet Type','Pick','Confidence%','Result','Logged'])
                df['Confidence%'] = df['Confidence%'].apply(lambda x: f"{x:.2f}%")
                def _color(v):
                    if v == 'WON':    return 'background-color:#0d2d0d;color:#4ade80'
                    if v == 'LOST':   return 'background-color:#2d0d0d;color:#f87171'
                    return ''
                st.dataframe(df.style.map(_color, subset=['Result']),
                             hide_index=True, use_container_width=True)
            else:
                st.info("No predictions logged yet.")
        except Exception as e:
            st.info(f"Log unavailable: {e}")

    # ══════════════════════════════════════════════════════════
    #  TAB 6 — RESULTS
    # ══════════════════════════════════════════════════════════
    render_results_tab(tab_results)

    # ══════════════════════════════════════════════════════════
    #  TAB 7 — LEARNING
    # ══════════════════════════════════════════════════════════
    render_learning_tab(tab_learn)


if __name__ == "__main__":
    main()
