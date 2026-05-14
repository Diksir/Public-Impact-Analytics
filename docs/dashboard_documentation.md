# Dashboard Documentation

Disclaimer: This project is an independent governance analytics and civic-tech research platform based on publicly available information.

## Pages

- Executive Overview: summary KPIs, weighted scores, and evidence count.
- Infrastructure Analysis: infrastructure-related evidence and score comparison.
- Crisis Management Analysis: continuity and response indicators.
- Economic Impact Analysis: sectoral and institutional economic evidence.
- Youth Empowerment Analysis: skills, training, and capacity-building indicators.
- Public Utility Management: electricity distribution and essential-service management evidence.
- Governance Scorecards: radar chart and category score table.
- Timeline Analysis: evidence by year and category.
- Source Verification Page: source table and evidence-to-source audit.
- Methodology Page: formulas, weights, limitations, and interpretation rules.

## Interpretation Rules

Scores are not campaign endorsements. They are weighted summaries of the available public evidence in the dataset.

Missing public evidence is marked as `insufficient_public_evidence`; it is not treated as a factual negative claim.

## Updating Data

1. Add sources to `data/raw/sources.csv`.
2. Add evidence rows to `data/raw/evidence_ledger.csv`.
3. Run `python scripts/build_datasets.py`.
4. Run `python scripts/generate_reports.py`.
5. Restart Streamlit.

