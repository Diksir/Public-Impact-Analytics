# Governance Performance Analytics Platform

This project is an independent governance analytics and civic-tech research platform based on publicly available information.

It compares publicly documented governance, institutional leadership, and public-service delivery indicators associated with:

- Dr. Jamilu Isyaku Gwamna
- Prof. Isa Ali Ibrahim Pantami
- Hon. Saidu Ahmed Alkali

The platform is neutral, evidence-based, and designed for civic research. It does not make campaign claims, does not infer criminality or misconduct, and does not treat missing data as evidence of poor performance.

## What Is Included

- Streamlit governance analytics dashboard
- Clean CSV datasets and Excel workbook
- Python preprocessing, cleaning, scoring, and report-generation scripts
- Governance scoring engine with transparent formulas
- Source verification table
- APA and MLA citation exports
- Downloadable Word reports:
  - `governance_report.docx`
  - `methodology.docx`
  - `references.docx`
- Social-media infographic CSV/PNG-ready data
- Tableau/Power BI-ready exports
- Transportation policy dashboard for rail, logistics, public transport reform, and transport-sector accountability evidence

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\build_datasets.py
python scripts\generate_reports.py
streamlit run app\dashboard.py
```

If you prefer the bundled Codex Python runtime, run the same scripts with the runtime path shown by Codex.

## Dashboard Pages

1. Executive Overview
2. Infrastructure Analysis
3. Crisis Management Analysis
4. Economic Impact Analysis
5. Youth Empowerment Analysis
6. Public Utility Management
7. Governance Scorecards
8. Timeline Analysis
9. Source Verification Page
10. Methodology Page

## Scoring Model

The weighted governance score uses:

- Infrastructure: 20%
- Economy: 20%
- Youth Empowerment: 20%
- Crisis Handling: 15%
- Transparency: 10%
- Public Utility Management: 10%
- Innovation: 5%

Scores are calculated only from evidence rows with source metadata. Where public evidence is insufficient, the system marks the row as `insufficient_public_evidence` and excludes it from score inflation.

## Legal And Research Disclaimer

This project is an independent governance analytics and civic-tech research platform based on publicly available information.

All claims are tied to source records. Scores are analytical estimates based on the stated methodology, not definitive judgments of personal character or overall public worth.
