# Governance Performance Analytics Platform

This platform is an independent civic-tech and governance analytics research project based on publicly available information and evidence-based analysis. It does not represent any political party, candidate, or government institution.

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
- Full life-cycle leadership profiles covering early background, education, early career, professional growth, major leadership roles, achievements, public impact, controversies or limitations, and current relevance
- Leadership Journey Timeline dataset using `candidate_name`, `life_stage`, `year_or_period`, `role_or_event`, `institution`, `sector`, `achievement`, `evidence`, `citation`, `impact_category`, and `impact_score`

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
2. Leadership Profiles
3. Infrastructure Analysis
4. Crisis Management Analysis
5. Economic Impact Analysis
6. Youth Empowerment Analysis
7. Public Utility Management
8. Governance Scorecards
9. Leadership Journey Timeline
10. Source Verification Page
11. Methodology Page

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

All claims are tied to source records. Scores are analytical estimates based on the stated methodology, not definitive judgments of personal character or overall public worth. Childhood or personal background information is included only when publicly available, verifiable, and cited.
