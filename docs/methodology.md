# Methodology

This project uses an evidence-led scoring model.

Formula:

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

