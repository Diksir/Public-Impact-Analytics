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

DISCLAIMER = (
    "This project is an independent governance analytics and civic-tech research "
    "platform based on publicly available information."
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

LEADER_COLORS = ["#68d85f", "#5f8cff", "#f4bd3c", "#28c4b7", "#ff8a3c"]

CATEGORY_LABELS = {
    "Infrastructure": "Infrastructure Development",
    "Economy": "Economic Impact",
    "Youth Empowerment": "Youth Empowerment",
    "Crisis Handling": "Crisis Management",
    "Transparency": "Transparency & Accountability",
    "Public Utility Management": "Public Utilities",
    "Innovation": "Innovation & Digital Impact",
}

PAGE_TO_CATEGORY = {
    "Infrastructure": "Infrastructure",
    "Economy": "Economy",
    "Youth Empowerment": "Youth Empowerment",
    "Crisis Management": "Crisis Handling",
    "Public Utilities": "Public Utility Management",
}

PAGE_NAMES = [
    "Overview",
    "Executive Summary",
    "Infrastructure",
    "Transportation Policy",
    "Economy",
    "Youth Empowerment",
    "Crisis Management",
    "Public Utilities",
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
    with ZipFile(zip_path, "w") as archive:
        for path in EXPORTS.glob("*"):
            if path.is_file() and path.name != zip_path.name:
                archive.write(path, path.name)
    return zip_path


def local_css():
    hero_url = ""
    if HERO_IMAGE.exists():
        encoded = base64.b64encode(HERO_IMAGE.read_bytes()).decode("ascii")
        hero_url = f"data:image/png;base64,{encoded}"
    css = """
        <style>
        :root {
          --bg: #07111f;
          --panel: #101d32;
          --panel-2: #13243d;
          --line: rgba(154, 180, 220, 0.18);
          --muted: #aebbd0;
          --text: #f6f8fc;
          --gold: #f4bd3c;
          --green: #6fd567;
          --blue: #5f8cff;
          --cyan: #28c4b7;
          --orange: #ff8a3c;
        }

        html, body, .stApp {
          background: radial-gradient(circle at 42% 2%, #1c3455 0, #07111f 42%, #040a13 100%) !important;
          color: var(--text);
        }

        .block-container {
          padding: 1.1rem 1.15rem 1.4rem 1.15rem;
          max-width: 1600px;
        }

        [data-testid="stHeader"] {
          background: transparent;
          height: 0;
        }

        [data-testid="stSidebar"] {
          background: linear-gradient(180deg, #06101d 0%, #07111f 100%);
          border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
          color: var(--text);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
          padding: 0.72rem 0.78rem;
          border-radius: 8px;
          margin: 0.18rem 0;
          border: 1px solid transparent;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
          background: rgba(244, 189, 60, 0.11);
          border-color: rgba(244, 189, 60, 0.35);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
          background: linear-gradient(135deg, #ffd567, #f4b735);
          color: #05101e !important;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) span {
          color: #05101e !important;
          font-weight: 700;
        }

        h1, h2, h3, h4, h5, h6, p, li, span, label {
          color: var(--text);
          letter-spacing: 0;
        }

        .platform-shell {
          border: 1px solid var(--line);
          border-radius: 10px;
          overflow: hidden;
          background: rgba(8, 18, 32, 0.74);
          box-shadow: 0 18px 50px rgba(0,0,0,0.32);
        }

        .hero {
          min-height: 315px;
          padding: 38px 40px;
          border: 1px solid var(--line);
          border-radius: 10px;
          background:
            linear-gradient(90deg, rgba(9, 18, 32, 0.94), rgba(13, 26, 45, 0.82) 48%, rgba(13, 26, 45, 0.48)),
            linear-gradient(140deg, rgba(244, 189, 60, 0.16), transparent 32%),
            url("__HERO_URL__");
          background-size: cover;
          background-position: center 48%;
          display: flex;
          align-items: center;
        }

        .hero h1 {
          margin: 0;
          max-width: 760px;
          font-size: clamp(2.2rem, 5vw, 4.6rem);
          line-height: 0.96;
          font-weight: 800;
        }

        .gold { color: var(--gold); }
        .muted { color: var(--muted); }
        .hero p {
          max-width: 650px;
          margin: 20px 0 26px 0;
          color: #e3e9f5;
          font-size: 1.02rem;
          line-height: 1.6;
        }

        .button-row {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }

        .primary-btn, .ghost-btn {
          display: inline-flex;
          align-items: center;
          gap: 12px;
          min-height: 42px;
          padding: 0 22px;
          border-radius: 7px;
          font-weight: 750;
          text-decoration: none !important;
          border: 1px solid rgba(244, 189, 60, 0.72);
        }
        .primary-btn { background: linear-gradient(135deg, #ffd365, #f4b735); color: #07111f !important; }
        .ghost-btn { background: rgba(11, 22, 38, 0.58); color: var(--text) !important; border-color: rgba(235, 241, 252, 0.38); }

        .panel {
          background: linear-gradient(180deg, rgba(19, 36, 61, 0.94), rgba(11, 22, 38, 0.94));
          border: 1px solid var(--line);
          border-radius: 10px;
          padding: 16px;
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }

        .panel h3 {
          margin: 0 0 14px 0;
          font-size: 1.05rem;
        }

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
          background: linear-gradient(150deg, #152947, #11213a);
          border: 1px solid rgba(154, 180, 220, 0.16);
          border-radius: 8px;
          padding: 14px 12px;
          text-align: center;
          min-height: 142px;
        }

        .avatar {
          width: 82px;
          height: 82px;
          margin: 0 auto 10px auto;
          border-radius: 999px;
          display: grid;
          place-items: center;
          background: linear-gradient(135deg, #d9e3f5, #f4bd3c);
          color: #07111f;
          font-weight: 900;
          font-size: 1.35rem;
          border: 3px solid rgba(255,255,255,0.72);
        }

        .leader-name {
          font-weight: 800;
          line-height: 1.22;
          min-height: 42px;
          font-size: 0.92rem;
        }

        .score-number {
          font-size: 1.85rem;
          font-weight: 900;
          color: var(--green);
          margin-top: 10px;
        }

        .score-scale { color: #dce6f7; font-size: 0.88rem; font-weight: 500; }
        .status-dot {
          width: 9px;
          height: 9px;
          display: inline-block;
          border-radius: 999px;
          background: var(--green);
          margin-right: 6px;
        }

        .kpi-row {
          display: grid;
          grid-template-columns: repeat(7, minmax(118px, 1fr));
          gap: 8px;
          margin-top: 12px;
        }

        .kpi-card {
          min-height: 154px;
          padding: 12px 10px;
          border-radius: 8px;
          border: 1px solid rgba(154, 180, 220, 0.22);
          background: linear-gradient(180deg, rgba(21, 40, 68, 0.88), rgba(14, 28, 49, 0.88));
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }

        .icon-badge {
          width: 46px;
          height: 46px;
          border-radius: 999px;
          display: grid;
          place-items: center;
          margin: 0 auto;
          font-size: 1.25rem;
          background: rgba(244, 189, 60, 0.12);
          border: 1px solid rgba(244, 189, 60, 0.32);
          color: var(--gold);
        }

        .kpi-title {
          text-align: center;
          color: #f5f8ff;
          font-size: 0.78rem;
          font-weight: 750;
          line-height: 1.28;
          min-height: 34px;
        }

        .kpi-scores {
          display: flex;
          justify-content: space-between;
          font-size: 1.05rem;
          font-weight: 900;
        }

        .green { color: var(--green); }
        .blue { color: var(--blue); }
        .gold-text { color: var(--gold); }

        .legend {
          display: flex;
          gap: 18px;
          margin: 12px 0 4px 0;
          color: var(--muted);
          flex-wrap: wrap;
          font-size: 0.9rem;
        }

        .legend-dot {
          width: 10px;
          height: 10px;
          border-radius: 999px;
          display: inline-block;
          margin-right: 6px;
        }

        .side-list {
          display: grid;
          gap: 10px;
        }

        .source-row, .download-row-item, .achievement-row {
          display: grid;
          grid-template-columns: 1fr auto auto;
          gap: 10px;
          align-items: center;
          padding: 8px 10px;
          border-radius: 7px;
          background: rgba(7, 17, 31, 0.42);
          color: #edf4ff;
        }
        .source-pill {
          min-width: 34px;
          text-align: center;
          background: rgba(95, 140, 255, 0.25);
          color: #cfe0ff;
          padding: 2px 8px;
          border-radius: 5px;
          font-weight: 800;
        }
        .check { color: var(--green); font-weight: 900; }

        .achievement-row {
          grid-template-columns: 46px 1fr;
          min-height: 62px;
        }
        .achievement-icon {
          width: 38px;
          height: 38px;
          display: grid;
          place-items: center;
          border-radius: 999px;
          border: 1px solid rgba(244, 189, 60, 0.5);
          color: var(--gold);
          background: rgba(244, 189, 60, 0.10);
          font-weight: 900;
        }
        .achievement-title { font-weight: 800; font-size: 0.86rem; }
        .achievement-copy { color: var(--muted); font-size: 0.76rem; line-height: 1.35; }

        .footer-note {
          border-top: 1px solid var(--line);
          padding: 14px 18px;
          color: var(--muted);
          font-size: 0.82rem;
        }

        .stDataFrame, [data-testid="stDataFrame"] {
          background: var(--panel);
          border-radius: 10px;
        }

        div[data-testid="stDownloadButton"] > button,
        div[data-testid="stButton"] > button {
          background: rgba(7, 17, 31, 0.64);
          color: #eef4ff;
          border: 1px solid rgba(154, 180, 220, 0.24);
          border-radius: 7px;
          min-height: 40px;
        }

        div[data-testid="stDownloadButton"] > button:hover,
        div[data-testid="stButton"] > button:hover {
          border-color: rgba(244, 189, 60, 0.7);
          color: var(--gold);
        }

        @media (max-width: 1200px) {
          .kpi-row { grid-template-columns: repeat(2, minmax(130px, 1fr)); }
          .hero { min-height: 260px; padding: 28px 24px; }
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


def build_plot_theme(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 17, 31, 0.22)",
        font=dict(color="#dce6f7", family="Arial"),
        margin=dict(l=18, r=18, t=38, b=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(gridcolor="rgba(154,180,220,0.12)", zerolinecolor="rgba(154,180,220,0.15)")
    fig.update_yaxes(gridcolor="rgba(154,180,220,0.12)", zerolinecolor="rgba(154,180,220,0.15)")
    return fig


def radar_chart(category_scores: pd.DataFrame):
    fig = go.Figure()
    for i, (person, group) in enumerate(category_scores.groupby("person")):
        ordered = group.set_index("category").reindex(CATEGORIES).reset_index()
        fig.add_trace(
            go.Scatterpolar(
                r=ordered["category_score"].fillna(0),
                theta=[CATEGORY_LABELS.get(x, x) for x in ordered["category"]],
                fill="toself",
                name=person,
                line_color=LEADER_COLORS[i % len(LEADER_COLORS)],
                opacity=0.78,
            )
        )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(7, 17, 31, 0.22)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(154,180,220,0.22)"),
            angularaxis=dict(gridcolor="rgba(154,180,220,0.18)"),
        )
    )
    return build_plot_theme(fig, height=330)


def category_bar(category_scores: pd.DataFrame):
    fig = px.bar(
        category_scores,
        x="category",
        y="category_score",
        color="person",
        barmode="group",
        color_discrete_sequence=LEADER_COLORS,
        category_orders={"category": CATEGORIES},
        labels={"category_score": "Score", "category": ""},
    )
    fig.update_xaxes(ticktext=[CATEGORY_LABELS.get(c, c) for c in CATEGORIES], tickvals=CATEGORIES)
    fig.update_yaxes(range=[0, 100])
    return build_plot_theme(fig, height=330)


def trend_chart(timeline: pd.DataFrame, category_scores: pd.DataFrame):
    years = list(range(2019, 2025))
    traces = []
    for person, group in category_scores.groupby("person"):
        base = float(group["category_score"].mean())
        evidence_by_year = (
            timeline[timeline["person"].eq(person)]
            .dropna(subset=["metric_year"])
            .assign(metric_year=lambda df: df["metric_year"].astype(int))
            .groupby("metric_year")["confidence"]
            .sum()
        )
        values = []
        running = max(base - 12, 5)
        for year in years:
            running = min(100, running + float(evidence_by_year.get(year, 0)) * 6 + 1.7)
            values.append(round(running, 1))
        traces.append((person, values))

    fig = go.Figure()
    for i, (person, values) in enumerate(traces):
        fig.add_trace(
            go.Scatter(
                x=years,
                y=values,
                mode="lines+markers",
                name=person,
                line=dict(color=LEADER_COLORS[i % len(LEADER_COLORS)], width=2),
                marker=dict(size=7),
            )
        )
    fig.update_yaxes(range=[0, 100])
    return build_plot_theme(fig, height=330)


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
    st.sidebar.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    years = sorted([int(y) for y in data["evidence"]["metric_year"].dropna().unique()])
    period = st.sidebar.selectbox("Select Period", ["All Years"] + [str(y) for y in years])
    category = st.sidebar.selectbox("Category Filter", ["All Categories"] + CATEGORIES)
    st.sidebar.markdown(
        """
        <div style="margin-top:38px;padding:18px;border-radius:9px;background:linear-gradient(180deg,rgba(19,36,61,.84),rgba(10,21,37,.84));border:1px solid rgba(154,180,220,.18);">
          <div style="font-size:1.7rem;color:#6f7f96;">“</div>
          <div style="font-size:.9rem;line-height:1.65;color:#f6f8fc;">Good governance is measured through evidence, service delivery, and public accountability.</div>
          <div style="margin-top:14px;color:#f4bd3c;font-weight:800;font-size:.82rem;">- Civic Intelligence Initiative</div>
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
            <p>{DISCLAIMER} It compares measurable public-sector performance using verifiable data, research, and statistical analysis.</p>
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
    ordered = leader_scores.sort_values("person")
    cards = []
    for _, row in ordered.iterrows():
        score = float(row["overall_governance_score"])
        cards.append(
            f"<div class='leader-mini'>"
            f"<div class='avatar'>{initials(row['person'])}</div>"
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
    piv = category_scores.pivot_table(index="category", columns="person", values="category_score", aggfunc="mean")
    people = list(category_scores["person"].drop_duplicates())
    st.markdown('<h3 id="key-performance-indicators-overall">Key Performance Indicators <span class="muted">(Overall)</span></h3>', unsafe_allow_html=True)
    cards = []
    for cat in CATEGORIES:
        row = piv.loc[cat] if cat in piv.index else pd.Series(dtype=float)
        score_spans = []
        for idx, person in enumerate(people):
            value = float(row.get(person, 0))
            score_spans.append(
                f"<span style='color:{LEADER_COLORS[idx % len(LEADER_COLORS)]};'>{value:.1f}</span>"
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
    for idx, person in enumerate(people):
        legend_items.append(
            f"<span><span class='legend-dot' style='background:{LEADER_COLORS[idx % len(LEADER_COLORS)]};'></span>{person}</span>"
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
        st.plotly_chart(radar_chart(category_scores), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with bottom_mid:
        st.markdown('<div class="panel"><h3>Performance Trend Over Time</h3>', unsafe_allow_html=True)
        st.plotly_chart(trend_chart(data["timeline"], category_scores), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with bottom_right:
        render_achievements(evidence)

    st.markdown(f'<div class="footer-note">Disclaimer: {DISCLAIMER} It does not represent any political party, candidate, or government institution.</div>', unsafe_allow_html=True)


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
            color_discrete_sequence=LEADER_COLORS,
            labels={"category_score": "Score", "person": ""},
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(build_plot_theme(fig, height=360), use_container_width=True)
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


def page_transportation_policy(data: dict):
    st.markdown("<h2>Transportation Policy Dashboard</h2>", unsafe_allow_html=True)
    evidence = data["evidence"]
    alkali = evidence[evidence["person"].eq("Hon. Saidu Ahmed Alkali")].copy()
    transport_terms = (
        alkali["indicator"].str.contains("rail|transport|freight|policy|logistics|Kano|Kaduna|budget|FERMA", case=False, na=False)
        | alkali["claim_summary"].str.contains("rail|transport|freight|policy|logistics|Kano|Kaduna|budget|FERMA", case=False, na=False)
    )
    transport = alkali[transport_terms].copy()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Transport Evidence Rows", f"{len(transport):,}")
    c2.metric("Quantitative Rows", f"{int((transport['evidence_type'] == 'quantitative').sum()):,}")
    c3.metric("Rail/Infra Items", f"{int(transport['category'].eq('Infrastructure').sum()):,}")
    c4.metric("Policy/Innovation Items", f"{int(transport['category'].eq('Innovation').sum()):,}")

    left, right = st.columns([1.1, 1], gap="medium")
    with left:
        st.markdown('<div class="panel"><h3>Transport-Related Score Profile</h3>', unsafe_allow_html=True)
        alkali_scores = data["category_scores"][data["category_scores"]["person"].eq("Hon. Saidu Ahmed Alkali")]
        fig = px.bar(
            alkali_scores,
            x="category",
            y="category_score",
            color="category",
            color_discrete_sequence=LEADER_COLORS,
            category_orders={"category": CATEGORIES},
            labels={"category_score": "Score", "category": ""},
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(build_plot_theme(fig, height=360), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel"><h3>Policy And Reform Evidence</h3>', unsafe_allow_html=True)
        st.dataframe(
            transport[
                [
                    "category",
                    "indicator",
                    "metric_value",
                    "metric_unit",
                    "metric_year",
                    "evidence_type",
                    "confidence",
                    "source_id",
                ]
            ],
            hide_index=True,
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>Transportation Evidence Narrative</h3>', unsafe_allow_html=True)
    st.dataframe(
        transport[["indicator", "claim_summary", "attribution_note", "title", "url"]],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def page_scorecards(category_scores: pd.DataFrame):
    st.markdown('<h2 id="governance-scorecards">Governance Scorecards</h2>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="medium")
    with left:
        st.markdown('<div class="panel"><h3>Radar Scorecard</h3>', unsafe_allow_html=True)
        st.plotly_chart(radar_chart(category_scores), use_container_width=True)
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


def page_timeline(timeline: pd.DataFrame, category_scores: pd.DataFrame):
    st.markdown("<h2>Timeline Analysis</h2>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><h3>Evidence Timeline</h3>', unsafe_allow_html=True)
    clean = timeline.dropna(subset=["metric_year"]).copy()
    clean["metric_year"] = clean["metric_year"].astype(int)
    fig = px.scatter(
        clean,
        x="metric_year",
        y="category",
        color="person",
        symbol="category",
        hover_data=["indicator", "source_id", "confidence"],
        color_discrete_sequence=["#68d85f", "#5f8cff"],
    )
    st.plotly_chart(build_plot_theme(fig, height=430), use_container_width=True)
    st.dataframe(timeline, use_container_width=True, hide_index=True)
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
    evidence, category_scores = filtered_data(data, period, selected_category)

    if page in {"Overview", "Executive Summary"}:
        page_overview(data, category_scores, evidence)
    elif page == "Transportation Policy":
        page_transportation_policy(data)
    elif page in PAGE_TO_CATEGORY:
        page_category(page, PAGE_TO_CATEGORY[page], data["category_scores"], evidence)
    elif page == "Governance Scorecard":
        page_scorecards(data["category_scores"])
    elif page == "Timeline Analysis":
        page_timeline(data["timeline"], data["category_scores"])
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
