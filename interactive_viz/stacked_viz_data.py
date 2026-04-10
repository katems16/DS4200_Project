import pandas as pd
import json

df = pd.read_csv("healthcare_cleaned.csv")

conditions = sorted(df['medical_condition'].dropna().unique().tolist())
hospitals_per_condition = {}

for cond in conditions:
    sub = df[df['medical_condition'] == cond]
    top_hospitals = (
        sub.groupby('hospital').size()
        .sort_values(ascending=False)
        .head(10).index.tolist()
    )
    sub = sub[sub['hospital'].isin(top_hospitals)]
    agg = (
        sub.groupby(['hospital', 'insurance_provider'])['billing_amount']
        .mean().reset_index()
    )
    hospitals_per_condition[cond] = agg.to_dict(orient='records')

with open("interactive_bar_data.js", "w") as f:
    f.write("const VIZ5_DATA = " + json.dumps(hospitals_per_condition) + ";")

print("Done. Conditions found:", conditions)
