import base64
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
EXPORTS = ROOT / "data" / "exports"
HERO_IMAGE = ROOT / "assets" / "images" / "gombe-hero.png"
LEADER_IMAGES = {
    "Dr. Jamilu Isyaku Gwamna": ROOT / "assets" / "images" / "jamilu-gwamna.jpg",
    "Hon. Saidu Ahmed Alkali": ROOT / "assets" / "images" / "saidu-alkali.jpg",
    "Prof. Isa Ali Ibrahim Pantami": ROOT / "assets" / "images" / "pantami.jpeg",
}

DISCLAIMER = (
    "This platform is an independent civic-tech and governance analytics research "
    "project based on publicly available information and evidence-based analysis. "
    "It does not represent any political party, candidate, or government institution."
)

CATEGORIES = [
    "Infrastructure",
    "Economy",
    "Youth Empowerment",
    "Crisis Handling",
    "Transparency",
    "Public Utility Management",
    "Innovation",
]

LEADER_ORDER = [
    "Prof. Isa Ali Ibrahim Pantami",
    "Dr. Jamilu Isyaku Gwamna",
    "Hon. Saidu Ahmed Alkali",
]
LEADER_COLORS = ["#68d85f", "#5f8cff", "#f4bd3c", "#28c4b7", "#ff8a3c"]
LEADER_COLOR_MAP = {
    leader: LEADER_COLORS[index % len(LEADER_COLORS)]
    for index, leader in enumerate(LEADER_ORDER)
}

CATEGORY_LABELS = {
    "Infrastructure": "Infrastructure Development",
    "Economy": "Economic Impact",
    "Youth Empowerment": "Youth Empowerment",
    "Crisis Handling": "Crisis Management",
    "Transparency": "Transparency & Accountability",
    "Public Utility Management": "Service Delivery",
    "Innovation": "Innovation & Digital Impact",
}

PAGE_TO_CATEGORY = {
    "Infrastructure": "Infrastructure",
    "Economy": "Economy",
    "Youth Empowerment": "Youth Empowerment",
    "Crisis Management": "Crisis Handling",
}

PAGE_NAMES = [
    "Overview",
    "Executive Summary",
    "Leadership Profiles",
    "Infrastructure",
    "Economy",
    "Youth Empowerment",
    "Crisis Management",
    "Governance Scorecard",
    "Timeline Analysis",
    "Source Verification",
    "Methodology",
    "Downloads",
    "About Project",
]

st.set_page_config(
    page_title="Governance Intelligence Platform",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data(data_version: float):
    return {
        "evidence": pd.read_csv(DATA / "clean_evidence_ledger.csv"),
        "sources": pd.read_csv(DATA / "source_verification_table.csv"),
        "category_scores": pd.read_csv(DATA / "category_scores.csv"),
        "leader_scores": pd.read_csv(DATA / "leader_scores.csv"),
        "timeline": pd.read_csv(DATA / "timeline.csv"),
        "weights": pd.read_csv(DATA / "scoring_weights.csv"),
    }


def data_version() -> float:
    files = [
        DATA / "clean_evidence_ledger.csv",
        DATA / "source_verification_table.csv",
        DATA / "category_scores.csv",
        DATA / "leader_scores.csv",
        DATA / "timeline.csv",
        DATA / "scoring_weights.csv",
    ]
    return sum(path.stat().st_mtime for path in files if path.exists())


def ensure_dataset_zip() -> Path:
    zip_path = EXPORTS / "all_governance_datasets.zip"
    source_files = [
        path for path in EXPORTS.glob("*")
        if path.is_file() and path.name != zip_path.name
    ]
    if zip_path.exists() and source_files:
        zip_mtime = zip_path.stat().st_mtime
        if all(path.stat().st_mtime <= zip_mtime for path in source_files):
            return zip_path
    with ZipFile(zip_path, "w") as archive:
        for path in source_files:
            archive.write(path, path.name)
    return zip_path


def local_css():
    hero_url = ""
    if HERO_IMAGE.exists():
        encoded = base64.b64encode(HERO_IMAGE.read_bytes()).decode("ascii")
        hero_url = f"data:image/png;base64,{encoded}"

    # Inject viewport meta tag so phones don't zoom-fit the desktop layout
    st.markdown(
        """<script>
        (function(){
          var m=document.querySelector('meta[name="viewport"]');
          if(!m){m=document.createElement('meta');m.name='viewport';document.head.appendChild(m);}
          m.content='width=device-width,initial-scale=1.0,maximum-scale=5.0,user-scalable=yes';
        })();
        </script>""",
        unsafe_allow_html=True,
    )

    css = """
        <style>
        /* =====================================================
           DESIGN TOKENS
           ===================================================== */
        :root {
          --bg: #07050d;
          --panel: #12101a;
          --panel-2: #1b1728;
          --line: rgba(190, 174, 225, 0.18);
          --muted: #b8b0c8;
          --text: #f6f8fc;
          --gold: #d8b45a;
          --green: #6fd567;
          --blue: #5f8cff;
          --cyan: #28c4b7;
          --orange: #ff8a3c;
          --transition: border-color 0.18s ease, background-color 0.18s ease, color 0.18s ease;
          --radius-sm: 8px;
          --radius-md: 12px;
        }

        /* =====================================================
           BASE — PREVENT HORIZONTAL SCROLL
           ===================================================== */
        html {
          scroll-behavior: smooth;
          -webkit-text-size-adjust: 100%;
          text-size-adjust: 100%;
          overflow-x: hidden;
        }

        html, body, .stApp {
          background:
            radial-gradient(circle at 18% 4%, rgba(84, 63, 130, 0.36) 0, rgba(84, 63, 130, 0.08) 28%, transparent 46%),
            radial-gradient(circle at 86% 10%, rgba(45, 37, 70, 0.38) 0, transparent 38%),
            linear-gradient(135deg, #05040a 0%, #0b0712 55%, #14101f 100%) !important;
          color: var(--text);
          overflow-x: hidden !important;
        }

        /* =====================================================
           STREAMLIT CHROME
           ===================================================== */
        [data-testid="stHeader"] { background: transparent; height: 0; }
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        #MainMenu,
        header button[kind="header"],
        header [data-testid="baseButton-header"] {
          display: none !important;
          visibility: hidden !important;
        }

        .block-container {
          padding: 1.1rem 1.15rem 1.4rem 1.15rem;
          max-width: 1600px;
        }

        /* =====================================================
           SIDEBAR
           ===================================================== */
        [data-testid="stSidebar"] {
          background: linear-gradient(180deg, #05040a 0%, #0b0712 55%, #100c18 100%);
          border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span { color: var(--text); }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
          padding: 0.72rem 0.78rem;
          border-radius: var(--radius-sm);
          margin: 0.18rem 0;
          border: 1px solid transparent;
          cursor: pointer;
          transition: var(--transition);
          min-height: 44px;
          display: flex;
          align-items: center;
          touch-action: manipulation;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
          background: rgba(216, 180, 90, 0.10);
          border-color: rgba(216, 180, 90, 0.30);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
          background: linear-gradient(135deg, #ffd567, #f4b735);
          color: #05101e !important;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) span {
          color: #05101e !important;
          font-weight: 700;
        }

        /* =====================================================
           TYPOGRAPHY
           ===================================================== */
        h1, h2, h3, h4, h5, h6, p, li, span, label {
          color: var(--text);
          letter-spacing: 0;
        }

        h2 { font-size: clamp(1.35rem, 3.5vw, 2rem); }
        h3 { font-size: clamp(0.92rem, 2vw, 1.08rem); }

        /* =====================================================
           PANELS — GLASSMORPHISM
           ===================================================== */
        .platform-shell {
          border: 1px solid var(--line);
          border-radius: 10px;
          overflow: hidden;
          background: rgba(10, 8, 16, 0.78);
          box-shadow: 0 18px 50px rgba(0,0,0,0.32);
        }

        .panel {
          background: linear-gradient(180deg, rgba(27, 23, 40, 0.92), rgba(12, 10, 18, 0.94));
          border: 1px solid rgba(190, 174, 225, 0.16);
          border-radius: var(--radius-md);
          padding: 18px;
          box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.05),
            0 8px 32px rgba(0,0,0,0.28);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
        }

        .panel h3 {
          margin: 0 0 14px 0;
          font-size: 1.05rem;
          letter-spacing: -0.01em;
        }

        /* =====================================================
           HERO
           ===================================================== */
        .hero {
          min-height: 315px;
          padding: 38px 40px;
          border: 1px solid var(--line);
          border-radius: var(--radius-md);
          background:
            linear-gradient(90deg, rgba(5, 4, 10, 0.95), rgba(12, 9, 20, 0.84) 48%, rgba(20, 16, 31, 0.56)),
            linear-gradient(140deg, rgba(216, 180, 90, 0.12), transparent 32%),
            url("__HERO_URL__");
          background-size: cover;
          background-position: center 48%;
          display: flex;
          align-items: center;
        }

        .hero h1 {
          margin: 0;
          max-width: 760px;
          font-size: clamp(1.8rem, 5vw, 4.6rem);
          line-height: 0.97;
          font-weight: 800;
          letter-spacing: -0.02em;
        }

        .gold { color: var(--gold); }
        .muted { color: var(--muted); }

        .hero p {
          max-width: 650px;
          margin: 18px 0 24px 0;
          color: #e3e9f5;
          font-size: clamp(0.84rem, 1.8vw, 1.02rem);
          line-height: 1.6;
        }

        /* =====================================================
           BUTTONS — TOUCH-FRIENDLY
           ===================================================== */
        .button-row {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .primary-btn, .ghost-btn {
          display: inline-flex;
          align-items: center;
          gap: 10px;
          min-height: 44px;
          padding: 0 22px;
          border-radius: var(--radius-sm);
          font-weight: 700;
          text-decoration: none !important;
          border: 1px solid rgba(244, 189, 60, 0.72);
          cursor: pointer;
          transition: var(--transition);
          touch-action: manipulation;
          -webkit-tap-highlight-color: transparent;
        }

        .primary-btn {
          background: linear-gradient(135deg, #ffd365, #f4b735);
          color: #07111f !important;
        }

        .primary-btn:hover {
          background: linear-gradient(135deg, #f6d77a, #d8b45a);
          box-shadow: 0 4px 18px rgba(216,180,90,0.20);
        }

        .ghost-btn {
          background: rgba(12, 10, 18, 0.66);
          color: var(--text) !important;
          border-color: rgba(224, 216, 242, 0.28);
        }

        .ghost-btn:hover {
          border-color: rgba(244, 189, 60, 0.5);
          background: rgba(244, 189, 60, 0.08);
        }

        /* =====================================================
           SCORE CARDS
           ===================================================== */
        .score-card {
          min-height: 236px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }

        .score-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(118px, 1fr));
          gap: 12px;
          align-items: stretch;
        }

        .leader-mini {
          background: linear-gradient(150deg, rgba(31, 26, 46, 0.96), rgba(16, 13, 24, 0.96));
          border: 1px solid rgba(190, 174, 225, 0.15);
          border-radius: var(--radius-sm);
          padding: 14px 12px;
          text-align: center;
          min-height: 142px;
          transition: var(--transition);
        }

        .leader-mini:hover {
          border-color: rgba(216, 180, 90, 0.30);
        }

        .avatar {
          width: 76px;
          height: 76px;
          margin: 0 auto 10px auto;
          border-radius: 999px;
          display: grid;
          place-items: center;
          background: linear-gradient(135deg, #d9e3f5, #f4bd3c);
          color: #07111f;
          font-weight: 900;
          font-size: 1.25rem;
          border: 3px solid rgba(255,255,255,0.72);
          box-shadow: 0 4px 14px rgba(0,0,0,0.3);
          overflow: hidden;
        }

        .avatar img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }

        .leader-name {
          font-weight: 800;
          line-height: 1.22;
          min-height: 42px;
          font-size: 0.9rem;
        }

        .score-number {
          font-size: 1.8rem;
          font-weight: 900;
          color: var(--green);
          margin-top: 10px;
        }

        .score-scale { color: #dce6f7; font-size: 0.86rem; font-weight: 500; }

        .status-dot {
          width: 8px;
          height: 8px;
          display: inline-block;
          border-radius: 999px;
          background: var(--green);
          margin-right: 6px;
        }

        /* =====================================================
           KPI CARDS — RESPONSIVE GRID
           ===================================================== */
        .kpi-row {
          display: grid;
          grid-template-columns: repeat(7, minmax(100px, 1fr));
          gap: 8px;
          margin-top: 12px;
        }

        .kpi-card {
          min-height: 150px;
          padding: 12px 10px;
          border-radius: var(--radius-sm);
          border: 1px solid rgba(190, 174, 225, 0.18);
          background: linear-gradient(180deg, rgba(30, 26, 45, 0.92), rgba(15, 12, 22, 0.94));
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          transition: var(--transition);
          backdrop-filter: blur(4px);
          -webkit-backdrop-filter: blur(4px);
        }

        .kpi-card:hover {
          border-color: rgba(216, 180, 90, 0.36);
        }

        .icon-badge {
          width: 42px;
          height: 42px;
          border-radius: 999px;
          display: grid;
          place-items: center;
          margin: 0 auto;
          font-size: 0.7rem;
          font-weight: 800;
          background: rgba(216, 180, 90, 0.12);
          border: 1px solid rgba(216, 180, 90, 0.32);
          color: var(--gold);
          letter-spacing: 0.02em;
        }

        .kpi-title {
          text-align: center;
          color: #f5f8ff;
          font-size: 0.74rem;
          font-weight: 700;
          line-height: 1.28;
          min-height: 32px;
        }

        .kpi-scores {
          display: flex;
          justify-content: space-between;
          font-size: 1.0rem;
          font-weight: 900;
          flex-wrap: wrap;
          gap: 2px;
        }

        /* =====================================================
           UTILITIES
           ===================================================== */
        .green { color: var(--green); }
        .blue { color: var(--blue); }
        .gold-text { color: var(--gold); }

        .legend {
          display: flex;
          gap: 18px;
          margin: 12px 0 4px 0;
          color: #f2f4fb;
          flex-wrap: wrap;
          font-size: 0.88rem;
          align-items: center;
        }

        .legend span {
          color: #f2f4fb !important;
          font-weight: 700;
          text-shadow: 0 1px 2px rgba(0,0,0,0.45);
        }

        .legend-dot {
          width: 10px;
          height: 10px;
          border-radius: 999px;
          display: inline-block;
          margin-right: 6px;
        }

        /* =====================================================
           SOURCE / ACHIEVEMENT ROWS
           ===================================================== */
        .side-list { display: grid; gap: 8px; }

        .source-row, .download-row-item, .achievement-row {
          display: grid;
          grid-template-columns: 1fr auto auto;
          gap: 10px;
          align-items: center;
          padding: 8px 10px;
          border-radius: 7px;
          background: rgba(10, 8, 16, 0.56);
          color: #edf4ff;
          transition: var(--transition);
        }

        .source-row:hover { background: rgba(216, 180, 90, 0.06); }

        .source-pill {
          min-width: 34px;
          text-align: center;
          background: rgba(95, 140, 255, 0.18);
          color: #cfe0ff;
          padding: 2px 8px;
          border-radius: 5px;
          font-weight: 800;
        }

        .check { color: var(--green); font-weight: 900; }

        .achievement-row {
          grid-template-columns: 46px 1fr;
          min-height: 60px;
        }

        .achievement-icon {
          width: 36px;
          height: 36px;
          display: grid;
          place-items: center;
          border-radius: 999px;
          border: 1px solid rgba(244, 189, 60, 0.5);
          color: var(--gold);
          background: rgba(216, 180, 90, 0.10);
          font-weight: 900;
          font-size: 0.88rem;
        }

        .achievement-title { font-weight: 800; font-size: 0.84rem; }
        .achievement-copy { color: var(--muted); font-size: 0.74rem; line-height: 1.35; }

        /* =====================================================
           FOOTER
           ===================================================== */
        .footer-note {
          border-top: 1px solid var(--line);
          padding: 14px 18px;
          color: var(--muted);
          font-size: 0.8rem;
          line-height: 1.5;
        }

        /* =====================================================
           STREAMLIT NATIVE ELEMENTS
           ===================================================== */
        .stDataFrame, [data-testid="stDataFrame"] {
          background: var(--panel);
          border-radius: 10px;
          overflow-x: auto !important;
          -webkit-overflow-scrolling: touch !important;
        }

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stButton"] > button {
          background: rgba(10, 8, 16, 0.72);
          color: #eef4ff;
          border: 1px solid rgba(154, 180, 220, 0.24);
          border-radius: var(--radius-sm);
          min-height: 42px;
          cursor: pointer;
          transition: var(--transition);
          touch-action: manipulation;
          font-weight: 600;
          -webkit-tap-highlight-color: transparent;
        }

        div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stButton"] > button:hover {
          border-color: rgba(244, 189, 60, 0.7);
          color: var(--gold);
          background: rgba(216, 180, 90, 0.07);
        }

        [data-testid="stSelectbox"] > div > div {
          background: rgba(10, 8, 16, 0.70) !important;
          border: 1px solid rgba(154, 180, 220, 0.22) !important;
          border-radius: var(--radius-sm) !important;
          color: var(--text) !important;
        }

        /* Charts */
        .stPlotlyChart {
          border-radius: var(--radius-sm);
          overflow: visible !important;
          max-width: 100% !important;
          padding-bottom: 10px;
        }
        .js-plotly-plot { max-width: 100% !important; }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: rgba(10,8,16,0.6); }
        ::-webkit-scrollbar-thumb { background: rgba(216,180,90,0.34); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(216,180,90,0.52); }

        /* =====================================================
           BREAKPOINT: TABLET / SMALL LAPTOP (≤ 1200px)
           ===================================================== */
        @media (max-width: 1200px) {
          .kpi-row { grid-template-columns: repeat(4, 1fr); }
          .hero { min-height: 265px; padding: 30px 28px; }
        }

        /* =====================================================
           BREAKPOINT: MOBILE (≤ 768px)
           STACK COLUMNS, COMPACT EVERYTHING
           ===================================================== */
        @media (max-width: 768px) {
          /* No horizontal overflow at any level */
          html, body, .stApp, .block-container {
            overflow-x: hidden !important;
            max-width: 100vw !important;
          }

          .block-container {
            padding: 0.5rem 0.6rem 0.9rem 0.6rem !important;
            max-width: 100% !important;
          }

          /* STACK STREAMLIT COLUMNS */
          [data-testid="stHorizontalBlock"],
          [data-testid="stColumns"] {
            flex-direction: column !important;
            gap: 0.6rem !important;
          }

          [data-testid="column"],
          [data-testid="stColumn"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
          }

          /* Hero — compact mobile */
          .hero {
            min-height: 185px !important;
            padding: 20px 16px !important;
            border-radius: var(--radius-sm) !important;
            align-items: flex-start !important;
          }

          .hero h1 {
            font-size: clamp(1.42rem, 6.5vw, 2.1rem) !important;
            line-height: 1.06 !important;
          }

          .hero p {
            font-size: 0.8rem !important;
            margin: 10px 0 14px 0 !important;
            line-height: 1.5 !important;
          }

          /* Buttons — full-width stacked column */
          .button-row {
            flex-direction: column !important;
            gap: 8px !important;
            width: 100%;
          }

          .primary-btn, .ghost-btn {
            width: 100% !important;
            justify-content: center !important;
            min-height: 48px !important;
            font-size: 0.88rem !important;
            padding: 0 16px !important;
          }

          /* Panels */
          .panel {
            padding: 13px 12px !important;
            border-radius: var(--radius-sm) !important;
            margin-bottom: 0.5rem;
          }

          .panel h3 {
            font-size: 0.88rem !important;
            margin: 0 0 10px 0 !important;
          }

          /* KPI: 2-column grid */
          .kpi-row {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 6px !important;
            margin-top: 8px !important;
          }

          .kpi-card {
            min-height: 118px !important;
            padding: 10px 8px !important;
            border-radius: 6px !important;
          }

          .icon-badge {
            width: 34px !important;
            height: 34px !important;
            font-size: 0.6rem !important;
          }

          .kpi-title {
            font-size: 0.65rem !important;
            min-height: 26px !important;
          }

          .kpi-scores { font-size: 0.88rem !important; }

          /* Score cards */
          .score-card { min-height: unset !important; }

          .score-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
          }

          .leader-mini {
            min-height: 118px !important;
            padding: 12px 8px !important;
          }

          .avatar {
            width: 56px !important;
            height: 56px !important;
            font-size: 1rem !important;
            margin-bottom: 6px !important;
          }

          .leader-name { font-size: 0.73rem !important; min-height: 30px !important; }
          .score-number { font-size: 1.42rem !important; margin-top: 6px !important; }
          .score-scale { font-size: 0.7rem !important; }

          /* Legend */
          .legend { font-size: 0.76rem !important; gap: 8px !important; }
          .stPlotlyChart { padding-bottom: 18px !important; }

          /* Source rows */
          .source-row { font-size: 0.78rem !important; padding: 7px 8px !important; }

          /* Achievement rows */
          .achievement-row {
            grid-template-columns: 36px 1fr !important;
            min-height: 50px !important;
          }

          .achievement-icon { width: 28px !important; height: 28px !important; font-size: 0.72rem !important; }
          .achievement-title { font-size: 0.76rem !important; }
          .achievement-copy { font-size: 0.66rem !important; }

          /* Footer */
          .footer-note { padding: 10px 12px !important; font-size: 0.7rem !important; }

          /* Tables — touch-scrollable */
          .stDataFrame, [data-testid="stDataFrame"] { border-radius: 6px !important; }

          [data-testid="stDataFrame"] > div {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
          }

          /* Buttons */
          div[data-testid="stDownloadButton"] > button,
          div[data-testid="stButton"] > button {
            min-height: 48px !important;
            font-size: 0.86rem !important;
            width: 100% !important;
          }

          /* Sidebar toggle — large touch target */
          button[data-testid="stSidebarCollapseButton"],
          [data-testid="stSidebarCollapsedControl"] button {
            min-width: 44px !important;
            min-height: 44px !important;
          }

          h2 { font-size: 1.28rem !important; margin-bottom: 0.65rem !important; }
        }

        /* =====================================================
           BREAKPOINT: SMALL PHONE (≤ 480px)
           ===================================================== */
        @media (max-width: 480px) {
          .block-container {
            padding: 0.4rem 0.5rem 0.8rem 0.5rem !important;
          }

          .hero {
            min-height: 158px !important;
            padding: 16px 13px !important;
          }

          .hero h1 { font-size: 1.35rem !important; }

          .hero p {
            font-size: 0.76rem !important;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }

          .kpi-row { gap: 5px !important; }

          .kpi-card { min-height: 104px !important; padding: 8px 6px !important; }
          .icon-badge { width: 28px !important; height: 28px !important; }
          .kpi-title { font-size: 0.6rem !important; }
          .kpi-scores { font-size: 0.82rem !important; }

          .legend { font-size: 0.78rem !important; flex-direction: column !important; gap: 7px !important; align-items: flex-start !important; }
          .legend span { color: #f2f4fb !important; }
          .stPlotlyChart { padding-bottom: 24px !important; }

          .avatar { width: 48px !important; height: 48px !important; }
          .score-number { font-size: 1.28rem !important; }
        }

        /* =====================================================
           BREAKPOINT: LARGE SCREENS (≥ 1440px)
           ===================================================== */
        @media (min-width: 1440px) {
          .block-container { padding: 1.4rem 1.6rem 1.8rem 1.6rem; max-width: 1700px; }
          .hero { min-height: 360px; padding: 48px 56px; }
          .kpi-row { gap: 10px; }
          .kpi-card { min-height: 168px; padding: 14px 12px; }
          .panel { padding: 22px; }
        }

        /* =====================================================
           PRINT
           ===================================================== */
        @media print {
          [data-testid="stSidebar"] { display: none; }
          .block-container { max-width: 100%; padding: 0; }
          .hero { background: none !important; border: 1px solid #ccc; }
          .panel { backdrop-filter: none; -webkit-backdrop-filter: none; }
        }
        </style>
        """.replace("__HERO_URL__", hero_url)
    st.markdown(
        css,
        unsafe_allow_html=True,
    )


def compact_name(person: str) -> str:
    return (
        person.replace("Dr. ", "")
        .replace("Prof. ", "")
        .replace("Isa Ali Ibrahim ", "Isa Ali Ibrahim ")
    )


def initials(person: str) -> str:
    parts = [p[0] for p in person.replace(".", "").split() if p]
    return "".join(parts[:3]).upper()


def ordered_people(people) -> list[str]:
    available = list(dict.fromkeys([str(person) for person in people]))
    canonical = [person for person in LEADER_ORDER if person in available]
    extras = sorted([person for person in available if person not in LEADER_ORDER])
    return canonical + extras


def leader_color(person: str) -> str:
    if person not in LEADER_COLOR_MAP:
        return LEADER_COLORS[len(LEADER_COLOR_MAP) % len(LEADER_COLORS)]
    return LEADER_COLOR_MAP[person]


def ordered_leader_frame(df: pd.DataFrame) -> pd.DataFrame:
    ordered = ordered_people(df["person"].dropna().unique())
    return (
        df.assign(_leader_order=df["person"].map({person: idx for idx, person in enumerate(ordered)}))
        .sort_values(["_leader_order", "category"] if "category" in df.columns else ["_leader_order"])
        .drop(columns=["_leader_order"])
    )


def leader_avatar(person: str) -> str:
    image_path = LEADER_IMAGES.get(person)
    if image_path and image_path.exists():
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        suffix = image_path.suffix.lower()
        mime = "jpeg" if suffix in {".jpg", ".jpeg"} else "png"
        return f"<img src='data:image/{mime};base64,{encoded}' alt='{person}' />"
    return initials(person)


def score_status(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Strong"
    if score >= 40:
        return "Developing"
    return "Limited public evidence"


def source_summary(sources: pd.DataFrame) -> pd.DataFrame:
    rows = []
    mapping = {
        "government_publication": "Government Reports",
        "policy_document": "Ministry Publications",
        "regulator_report": "Regulator Reports",
        "verified_journalism": "News & Media Archives",
        "encyclopedia": "Other Verified Sources",
    }
    for source_type, label in mapping.items():
        count = int(sources["source_type"].eq(source_type).sum())
        if count:
            rows.append({"label": label, "count": count})
    rows.append({"label": "Public Records", "count": int(sources["reliability_tier"].eq("official").sum())})
    return pd.DataFrame(rows)


def build_plot_theme(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 17, 31, 0.22)",
        font=dict(color="#dce6f7", family="Arial", size=12),
        margin=dict(l=14, r=14, t=36, b=14),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="left",
            x=0,
            font=dict(size=12, color="#f2f4fb"),
            bgcolor="rgba(5,4,10,0.60)",
            bordercolor="rgba(190,174,225,0.18)",
            borderwidth=1,
        ),
        autosize=True,
    )
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="#12101a",
            bordercolor="rgba(216,180,90,0.35)",
            font=dict(color="#f2f4fb"),
        )
    )
    fig.update_xaxes(gridcolor="rgba(154,180,220,0.12)", zerolinecolor="rgba(154,180,220,0.15)")
    fig.update_yaxes(gridcolor="rgba(154,180,220,0.12)", zerolinecolor="rgba(154,180,220,0.15)")
    return fig


def radar_chart(category_scores: pd.DataFrame):
    fig = go.Figure()
    ordered_scores = ordered_leader_frame(category_scores)
    for person in ordered_people(ordered_scores["person"].dropna().unique()):
        group = ordered_scores[ordered_scores["person"].eq(person)]
        ordered = group.set_index("category").reindex(CATEGORIES).reset_index()
        fig.add_trace(
            go.Scatterpolar(
                r=ordered["category_score"].fillna(0),
                theta=[CATEGORY_LABELS.get(x, x) for x in ordered["category"]],
                fill="toself",
                name=person,
                line_color=leader_color(person),
                opacity=0.78,
            )
        )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(10, 8, 16, 0.36)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(242,244,251,0.22)",
                tickfont=dict(color="#f2f4fb", size=11),
            ),
            angularaxis=dict(
                gridcolor="rgba(242,244,251,0.16)",
                tickfont=dict(color="#f2f4fb", size=12),
            ),
        )
    )
    themed = build_plot_theme(fig, height=380)
    themed.update_layout(margin=dict(l=42, r=42, t=24, b=92))
    return themed


def category_bar(category_scores: pd.DataFrame):
    ordered_scores = ordered_leader_frame(category_scores)
    fig = px.bar(
        ordered_scores,
        x="category",
        y="category_score",
        color="person",
        barmode="group",
        color_discrete_map=LEADER_COLOR_MAP,
        category_orders={"category": CATEGORIES},
        labels={"category_score": "Score", "category": ""},
    )
    fig.update_xaxes(ticktext=[CATEGORY_LABELS.get(c, c) for c in CATEGORIES], tickvals=CATEGORIES)
    fig.update_yaxes(range=[0, 100])
    return build_plot_theme(fig, height=320)


def trend_chart(timeline: pd.DataFrame, category_scores: pd.DataFrame):
    parsed = pd.to_numeric(timeline["year_or_period"].astype(str).str.extract(r"(\d{4})", expand=False), errors="coerce")
    valid_years = parsed.dropna().astype(int)
    if valid_years.empty:
        years = list(range(2019, 2025))
    else:
        years = list(range(int(valid_years.min()), min(2026, int(valid_years.max())) + 1))
    traces = []
    ordered_scores = ordered_leader_frame(category_scores)
    for person in ordered_people(ordered_scores["person"].dropna().unique()):
        group = ordered_scores[ordered_scores["person"].eq(person)]
        base = float(group["category_score"].mean())
        evidence_by_year = (
            timeline[timeline["candidate_name"].eq(person)]
            .assign(metric_year=parsed[timeline["candidate_name"].eq(person)])
            .dropna(subset=["metric_year"])
            .assign(metric_year=lambda df: df["metric_year"].astype(int))
            .groupby("metric_year")["impact_score"]
            .mean()
        )
        values = []
        running = max(base - 12, 5)
        for year in years:
            running = min(100, running + float(evidence_by_year.get(year, 0)) / 18 + 1.2)
            values.append(round(running, 1))
        traces.append((person, values))

    fig = go.Figure()
    for person, values in traces:
        fig.add_trace(
            go.Scatter(
                x=years,
                y=values,
                mode="lines+markers",
                name=person,
                line=dict(color=leader_color(person), width=2),
                marker=dict(size=7),
            )
        )
    fig.update_yaxes(range=[0, 100])
    return build_plot_theme(fig, height=320)


def download_button(label: str, path: Path, mime: str):
    if path.exists():
        st.download_button(label, path.read_bytes(), file_name=path.name, mime=mime, use_container_width=True)
    else:
        st.button(f"{label} unavailable", disabled=True, use_container_width=True)


def render_sidebar(data: dict):
    st.sidebar.markdown(
        """
        <div style="padding: 12px 4px 18px 4px;">
          <div style="display:flex; gap:10px; align-items:center;">
            <div style="width:46px;height:46px;border-radius:999px;border:1px solid rgba(244,189,60,.7);display:grid;place-items:center;color:#f4bd3c;font-weight:900;">GI</div>
            <div>
              <div style="font-size:1.03rem;font-weight:900;line-height:1.18;">Gombe Governance<br/>Intelligence Platform</div>
              <div style="color:#f4bd3c;font-size:.78rem;margin-top:6px;">Evidence. Transparency. Impact.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio("Navigation", PAGE_NAMES, label_visibility="collapsed")
    period = "All Years"
    st.sidebar.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    category = st.sidebar.selectbox("Category Filter", ["All Categories"] + CATEGORIES)
    st.sidebar.markdown(
        """
        <style>
        .sidebar-quote { margin-top: 28px; padding: 16px; border-radius: 9px;
          background: linear-gradient(180deg,rgba(19,36,61,.84),rgba(10,21,37,.84));
          border: 1px solid rgba(154,180,220,.18); }
        @media (max-width: 768px) { .sidebar-quote { margin-top: 16px; padding: 12px; } }
        </style>
        <div class="sidebar-quote">
          <div style="font-size:1.6rem;color:#6f7f96;">"</div>
          <div style="font-size:.88rem;line-height:1.6;color:#f6f8fc;">Good governance is measured through evidence, service delivery, and public accountability.</div>
          <div style="margin-top:12px;color:#f4bd3c;font-weight:800;font-size:.8rem;">- Civic Intelligence Initiative</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return page, period, category


def filtered_data(data: dict, period: str, category: str):
    evidence = data["evidence"].copy()
    category_scores = data["category_scores"].copy()
    if period != "All Years":
        evidence = evidence[evidence["metric_year"].fillna("").astype(str).str.startswith(period)]
    if category != "All Categories":
        evidence = evidence[evidence["category"].eq(category)]
        category_scores = category_scores[category_scores["category"].eq(category)]
    return evidence, category_scores


def render_hero():
    st.markdown(
        f"""
        <div class="hero">
          <div>
            <h1>Evidence-Based Governance.<br/><span class="gold">Data-Driven Decisions.</span></h1>
            <p>{DISCLAIMER} It compares full leadership journeys and measurable public-sector performance using verifiable data, research, citations, and transparent scoring methods.</p>
            <div class="button-row">
              <a class="primary-btn" href="#key-performance-indicators-overall">Explore Dashboard <span>→</span></a>
              <a class="ghost-btn" href="#methodology">View Methodology</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_leadership_score(leader_scores: pd.DataFrame):
    ordered = ordered_leader_frame(leader_scores)
    cards = []
    for _, row in ordered.iterrows():
        score = float(row["overall_governance_score"])
        cards.append(
            f"<div class='leader-mini'>"
            f"<div class='avatar'>{leader_avatar(row['person'])}</div>"
            f"<div class='leader-name'>{row['person']}</div>"
            f"<div class='score-number'>{score:.1f}<span class='score-scale'> /100</span></div>"
            f"<div class='muted'><span class='status-dot'></span>{score_status(score)}</div>"
            f"</div>"
        )
    st.markdown(
        f"""
        <div class="panel score-card">
          <h3>Overall Leadership Score</h3>
          <div class="score-grid">{"".join(cards)}</div>
          <div style="margin-top:12px;">
            <a class="ghost-btn" style="width:100%;justify-content:center;" href="#governance-scorecards">View Detailed Scorecard</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(category_scores: pd.DataFrame):
    icons = {
        "Infrastructure": "III",
        "Economy": "GDP",
        "Youth Empowerment": "YTH",
        "Crisis Handling": "RSP",
        "Public Utility Management": "UTL",
        "Transparency": "AUD",
        "Innovation": "INN",
    }
    ordered_scores = ordered_leader_frame(category_scores)
    piv = ordered_scores.pivot_table(index="category", columns="person", values="category_score", aggfunc="mean")
    people = ordered_people(ordered_scores["person"].drop_duplicates())
    st.markdown('<h3 id="key-performance-indicators-overall">Key Performance Indicators <span class="muted">(Overall)</span></h3>', unsafe_allow_html=True)
    cards = []
    for cat in CATEGORIES:
        row = piv.loc[cat] if cat in piv.index else pd.Series(dtype=float)
        score_spans = []
        for idx, person in enumerate(people):
            value = float(row.get(person, 0))
            score_spans.append(
                f"<span style='color:{leader_color(person)};'>{value:.1f}</span>"
            )
        weight = category_scores.loc[category_scores["category"].eq(cat), "weight"].max()
        cards.append(
            f"<div class='kpi-card'>"
            f"<div class='icon-badge'>{icons.get(cat, 'KPI')}</div>"
            f"<div class='kpi-title'>{CATEGORY_LABELS.get(cat, cat)}<br/>({int(float(weight) * 100)}%)</div>"
            f"<div class='kpi-scores'>{''.join(score_spans)}</div>"
            f"</div>"
        )
    legend_items = []
    for person in people:
        legend_items.append(
            f"<span><span class='legend-dot' style='background:{leader_color(person)};'></span>{person}</span>"
        )
    st.markdown(
        f"""
        <div class="kpi-row">{"".join(cards)}</div>
        <div class="legend">
          {"".join(legend_items)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sources_panel(sources: pd.DataFrame):
    rows = []
    for _, row in source_summary(sources).iterrows():
        rows.append(
            f'<div class="source-row"><span>{row["label"]}</span><span class="source-pill">{int(row["count"])}</span><span class="check">✓</span></div>',
        )
    st.markdown(
        f'<div class="panel"><h3>Data Sources Overview</h3><div class="side-list">{"".join(rows)}</div></div>',
        unsafe_allow_html=True,
    )


def render_downloads_panel():
    zip_path = ensure_dataset_zip()
    st.markdown('<div class="panel"><h3>Reports & Downloads</h3>', unsafe_allow_html=True)
    download_button("Full Governance Report (DOCX)", REPORTS / "governance_report.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    download_button("Methodology & Scoring (DOCX)", REPORTS / "methodology.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    download_button("References & Citations (DOCX)", REPORTS / "references.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    download_button("Data Dictionary / Workbook (XLSX)", EXPORTS / "governance_analytics_dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    download_button("All Datasets (ZIP)", zip_path, "application/zip")
    st.markdown("</div>", unsafe_allow_html=True)


def render_achievements(evidence: pd.DataFrame):
    picks = evidence[evidence["evidence_type"].ne("insufficient_public_evidence")].head(4)
    rows = []
    for idx, (_, row) in enumerate(picks.iterrows(), start=1):
        rows.append(
            f"<div class='achievement-row'>"
            f"<div class='achievement-icon'>{idx}</div>"
            f"<div><div class='achievement-title'>{row['indicator']}</div>"
            f"<div class='achievement-copy'>{row['claim_summary']}</div></div>"
            f"</div>"
        )
    st.markdown(
        f"""
        <div class="panel">
          <h3>Top Evidence Items <span class="muted">(Summary)</span></h3>
          {"".join(rows)}
          <div style="margin-top:12px;"><a class="ghost-btn" style="width:100%;justify-content:center;" href="#source-verification">View All Evidence</a></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_overview(data: dict, category_scores: pd.DataFrame, evidence: pd.DataFrame):
    top_left, top_right = st.columns([2.55, 1], gap="medium")
    with top_left:
        render_hero()
        render_kpis(category_scores)
    with top_right:
        render_leadership_score(data["leader_scores"])
        st.write("")
        render_sources_panel(data["sources"])
        st.write("")
        render_downloads_panel()

    bottom_left, bottom_mid, bottom_right = st.columns([1.35, 1.2, 0.9], gap="medium")
    with bottom_left:
        st.markdown('<div class="panel"><h3>Category Performance Comparison</h3>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(category_scores), use_container_width=True, config={"responsive": True, "displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with bottom_mid:
        st.markdown('<div class="panel"><h3>Performance Trend Over Time</h3>', unsafe_allow_html=True)
        st.plotly_chart(trend_chart(data["timeline"], category_scores), use_container_width=True, config={"responsive": True, "displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with bottom_right:
        render_achievements(evidence)

    st.markdown(f'<div class="footer-note">Disclaimer: {DISCLAIMER}</div>', unsafe_allow_html=True)


def page_category(title: str, category: str, category_scores: pd.DataFrame, evidence: pd.DataFrame):
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    filtered_scores = category_scores[category_scores["category"].eq(category)]
    filtered_evidence = evidence[evidence["category"].eq(category)]
    c1, c2 = st.columns([1.05, 1], gap="medium")
    with c1:
        st.markdown('<div class="panel"><h3>Evidence-Backed Category Score</h3>', unsafe_allow_html=True)
        fig = px.bar(
            filtered_scores,
            x="person",
            y="category_score",
            color="person",
            color_discrete_map=LEADER_COLOR_MAP,
            category_orders={"person": ordered_people(filtered_scores["person"].dropna().unique())},
            labels={"category_score": "Score", "person": ""},
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(build_plot_theme(fig, height=320), use_container_width=True, config={"responsive": True, "displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><h3>Score Metadata</h3>', unsafe_allow_html=True)
        st.dataframe(
            filtered_scores[["person", "weight", "category_score", "evidence_count", "quantitative_count", "coverage_status"]],
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>How This Category Earned Its Points</h3>', unsafe_allow_html=True)
    explanation = filtered_scores.copy()
    explanation["weight_percent"] = (explanation["weight"] * 100).round(0).astype(int).astype(str) + "%"
    explanation["formula"] = (
        explanation["category_score"].round(2).astype(str)
        + " x "
        + explanation["weight"].round(2).astype(str)
        + " = "
        + explanation["weighted_points"].round(2).astype(str)
        + " overall points"
    )
    st.dataframe(
        explanation[
            [
                "person",
                "category_score",
                "weight_percent",
                "weighted_points",
                "evidence_count",
                "quantitative_count",
                "formula",
                "coverage_status",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Category score is the average of scored evidence rows. Weighted points are the category score multiplied by the category weight."
    )
    evidence_breakdown = filtered_evidence.copy()
    evidence_breakdown["scoring_effect"] = evidence_breakdown["evidence_type"].map(
        {
            "quantitative": "High scoring weight because it has a measurable value.",
            "project_report": "Medium scoring weight because it documents a project activity.",
            "regulator_context": "Medium scoring weight because it comes from regulator context.",
            "policy_target_context": "Medium scoring weight because it is policy target context.",
            "qualitative": "Lower scoring weight because it is narrative evidence.",
            "insufficient_public_evidence": "Not awarded positive points; kept as a data gap.",
        }
    ).fillna("Contextual evidence.")
    st.dataframe(
        evidence_breakdown[
            [
                "person",
                "indicator",
                "evidence_type",
                "metric_value",
                "metric_unit",
                "confidence",
                "evidence_score",
                "scoring_effect",
                "source_id",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Evidence Ledger</h3>', unsafe_allow_html=True)
    st.dataframe(
        filtered_evidence[
            [
                "person",
                "indicator",
                "metric_value",
                "metric_unit",
                "metric_year",
                "claim_summary",
                "source_id",
                "confidence",
                "data_quality_flag",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def page_scorecards(category_scores: pd.DataFrame):
    st.markdown('<h2 id="governance-scorecards">Governance Scorecards</h2>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="medium")
    with left:
        st.markdown('<div class="panel"><h3>Radar Scorecard</h3>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(category_scores), use_container_width=True, config={"responsive": True, "displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Weighted Category Table</h3>', unsafe_allow_html=True)
        st.dataframe(category_scores, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Category Points Formula</h3>', unsafe_allow_html=True)
    formula_table = category_scores.copy()
    formula_table["formula"] = (
        formula_table["category_score"].round(2).astype(str)
        + " x "
        + formula_table["weight"].round(2).astype(str)
        + " = "
        + formula_table["weighted_points"].round(2)
        .astype(str)
        + " points"
    )
    st.dataframe(
        formula_table[
            [
                "person",
                "category",
                "category_score",
                "weight",
                "weighted_points",
                "formula",
                "coverage_status",
            ]
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def parse_timeline_years(timeline: pd.DataFrame) -> pd.Series:
    return pd.to_numeric(timeline["year_or_period"].astype(str).str.extract(r"(\d{4})", expand=False), errors="coerce")


def source_options(sources: pd.DataFrame) -> dict:
    return sources.set_index("source_id")[["title", "organization", "url"]].to_dict("index")


def page_leadership_profiles(timeline: pd.DataFrame, sources: pd.DataFrame):
    st.markdown("<h2>Complete Leadership Profiles</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="panel">
          <h3>Research Boundary</h3>
          <p>{DISCLAIMER}</p>
          <p class="muted">Verified facts, reported public controversies, and analytical scoring are separated. Childhood, family or personal background details appear only when public, verifiable, and cited; otherwise the profile records a limitation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    coverage = (
        timeline.assign(has_positive_context=timeline["impact_score"].fillna(0).astype(float).gt(0))
        .groupby("candidate_name", as_index=False)
        .agg(
            lifecycle_rows=("life_stage", "count"),
            early_background_rows=("life_stage", lambda x: int((x == "Early background").sum())),
            education_rows=("life_stage", lambda x: int((x == "Education").sum())),
            early_career_rows=("life_stage", lambda x: int((x == "Early career").sum())),
            cited_sources=("citation", "nunique"),
            scored_context_rows=("has_positive_context", "sum"),
        )
    )
    st.markdown('<div class="panel"><h3>Lifecycle Coverage Snapshot</h3>', unsafe_allow_html=True)
    st.dataframe(coverage, use_container_width=True, hide_index=True)
    st.caption("This table shows coverage, not political preference. Lower early-life coverage means fewer verifiable public records were found, not a negative judgment.")
    st.markdown("</div>", unsafe_allow_html=True)

    candidate = st.selectbox("Candidate", ordered_people(timeline["candidate_name"].dropna().unique()))
    profile = timeline[timeline["candidate_name"].eq(candidate)].copy()
    citations = source_options(sources)

    stages = [
        "Early background",
        "Education",
        "Early career",
        "Professional growth",
        "Major leadership roles",
        "Political leadership",
        "Major achievements",
        "Community service",
        "Public impact",
        "Criticisms and controversies",
        "Criticisms and limitations",
        "Current relevance",
    ]
    cards = []
    for stage in stages:
        group = profile[profile["life_stage"].eq(stage)]
        if group.empty:
            continue
        items = []
        for _, row in group.iterrows():
            source = citations.get(row["citation"], {})
            link = source.get("url", "")
            source_label = f'{row["citation"]}: {source.get("organization", "Source")}'
            citation_html = f"<a href='{link}' target='_blank'>{source_label}</a>" if link else source_label
            items.append(
                f"<li><strong>{row['year_or_period']} - {row['role_or_event']}</strong><br/>"
                f"<span class='muted'>{row['institution']} | {row['sector']} | {citation_html}</span><br/>"
                f"{row['achievement']}</li>"
            )
        cards.append(
            f"<div class='panel'><h3>{stage}</h3><ul>{''.join(items)}</ul></div>"
        )
    st.markdown("".join(cards), unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Candidate Lifecycle Dataset</h3>', unsafe_allow_html=True)
    st.dataframe(profile, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_timeline(timeline: pd.DataFrame, sources: pd.DataFrame):
    st.markdown("<h2>Leadership Journey Timeline</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="medium")
    with c1:
        candidate_filter = st.selectbox("Candidate Timeline", ["All Candidates"] + ordered_people(timeline["candidate_name"].dropna().unique()))
    with c2:
        stage_filter = st.selectbox("Life Stage", ["All Life Stages"] + list(dict.fromkeys(timeline["life_stage"].dropna())))
    visible_timeline = timeline.copy()
    if candidate_filter != "All Candidates":
        visible_timeline = visible_timeline[visible_timeline["candidate_name"].eq(candidate_filter)]
    if stage_filter != "All Life Stages":
        visible_timeline = visible_timeline[visible_timeline["life_stage"].eq(stage_filter)]

    st.markdown('<div class="panel"><h3>Full Life-Cycle Leadership Timeline</h3>', unsafe_allow_html=True)
    clean = visible_timeline.copy()
    clean["metric_year"] = parse_timeline_years(clean)
    clean = clean.dropna(subset=["metric_year"])
    clean["metric_year"] = clean["metric_year"].astype(int)
    fig = px.scatter(
        clean,
        x="metric_year",
        y="life_stage",
        color="candidate_name",
        symbol="impact_category",
        size="impact_score",
        hover_data=["role_or_event", "institution", "citation", "impact_score"],
        color_discrete_map=LEADER_COLOR_MAP,
        category_orders={"candidate_name": ordered_people(clean["candidate_name"].dropna().unique())},
    )
    st.plotly_chart(build_plot_theme(fig, height=380), use_container_width=True, config={"responsive": True, "displayModeBar": False})
    enriched = visible_timeline.merge(
        sources[["source_id", "title", "organization", "url"]],
        left_on="citation",
        right_on="source_id",
        how="left",
    ).drop(columns=["source_id"])
    st.dataframe(visible_timeline, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Citations Beside Timeline Claims</h3>', unsafe_allow_html=True)
    st.dataframe(
        enriched[
            [
                "candidate_name",
                "life_stage",
                "year_or_period",
                "role_or_event",
                "evidence",
                "citation",
                "title",
                "organization",
                "url",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def page_sources(sources: pd.DataFrame, evidence: pd.DataFrame):
    st.markdown('<h2 id="source-verification">Source Verification</h2>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Source Register</h3>', unsafe_allow_html=True)
    st.dataframe(sources, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Evidence-To-Source Audit</h3>', unsafe_allow_html=True)
    st.dataframe(
        evidence[["evidence_id", "person", "category", "indicator", "source_id", "title", "organization", "url"]],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def page_methodology(weights: pd.DataFrame):
    st.markdown('<h2 id="methodology">Methodology</h2>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="panel">
          <h3>Scoring Formula</h3>
          <p>The scoring engine calculates an evidence score for each row, aggregates those rows by leader and category, then applies the agreed category weights.</p>
          <p><code>category_score = average(evidence_score for scored rows in category)</code></p>
          <p><code>weighted_points = category_score * category_weight</code></p>
          <p><code>overall_governance_score = sum(weighted_points across all categories)</code></p>
          <p class="muted">Evidence rows marked <code>insufficient_public_evidence</code> receive no positive score. This prevents the dashboard from manufacturing claims where public data is missing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="panel"><h3>Weights</h3>', unsafe_allow_html=True)
    st.dataframe(weights, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_downloads():
    cols = st.columns(2, gap="medium")
    with cols[0]:
        render_downloads_panel()
    with cols[1]:
        st.markdown('<div class="panel"><h3>Deployment Commands</h3>', unsafe_allow_html=True)
        st.code(
            r"""
.\.venv\Scripts\Activate.ps1
python scripts\build_datasets.py
python scripts\generate_reports.py
streamlit run app\dashboard.py
            """.strip(),
            language="powershell",
        )
        st.markdown("</div>", unsafe_allow_html=True)


def page_about():
    st.markdown("<h2>About Project</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="panel">
          <p>{DISCLAIMER}</p>
          <p>This platform is designed for neutral civic research. It compares documented evidence on institutional management, infrastructure, crisis handling, economic contribution, public utility management, and innovation.</p>
          <p class="muted">The dashboard does not generate propaganda, personal attacks, or unsupported statistics. Every scored claim is tied to source metadata in the evidence ledger.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    local_css()
    data = load_data(data_version())
    page, period, selected_category = render_sidebar(data)
    st.info(DISCLAIMER)
    evidence, category_scores = filtered_data(data, period, selected_category)

    if page in {"Overview", "Executive Summary"}:
        page_overview(data, category_scores, evidence)
    elif page == "Leadership Profiles":
        page_leadership_profiles(data["timeline"], data["sources"])
    elif page in PAGE_TO_CATEGORY:
        page_category(page, PAGE_TO_CATEGORY[page], data["category_scores"], evidence)
    elif page == "Governance Scorecard":
        page_scorecards(data["category_scores"])
    elif page == "Timeline Analysis":
        page_timeline(data["timeline"], data["sources"])
    elif page == "Source Verification":
        page_sources(data["sources"], evidence)
    elif page == "Methodology":
        page_methodology(data["weights"])
    elif page == "Downloads":
        page_downloads()
    else:
        page_about()


if __name__ == "__main__":
    main()
