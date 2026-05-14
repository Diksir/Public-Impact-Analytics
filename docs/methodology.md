# Methodology

This platform is an independent civic-tech and governance analytics research project based on publicly available information and evidence-based analysis. It does not represent any political party, candidate, or government institution.

The project uses an evidence-led scoring model and a separate full life-cycle leadership journey model.

## Leadership Journey Schema

The leadership timeline uses the following fields:

- `candidate_name`
- `life_stage`
- `year_or_period`
- `role_or_event`
- `institution`
- `sector`
- `achievement`
- `evidence`
- `citation`
- `impact_category`
- `impact_score`

Lifecycle rows cover early background, education, early career, professional growth, major leadership roles, major achievements, public impact, controversies or limitations, and current relevance. Childhood, family, or personal background details are included only when public, verifiable, and cited. Missing personal-background data is marked as a limitation and receives no positive score.

## Governance Score Formula

The scorecard formula is:

```text
category_score = average(evidence_score for scored evidence rows in category)
weighted_points = category_score * category_weight
overall_governance_score = sum(weighted_points)
```

Weights:

- Infrastructure = 20%
- Economy = 20%
- Youth Empowerment = 20%
- Crisis Handling = 15%
- Transparency = 10%
- Public Utility Management = 10%
- Innovation = 5%

Evidence scoring prioritizes quantitative regulator/government data over interviews or broad narrative claims. The model explicitly avoids fake statistics by preserving missing values and marking unsupported categories.
