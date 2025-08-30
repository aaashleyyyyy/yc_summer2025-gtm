#lead scoring for a b2b saas company 

import pandas as pd
import numpy as np

df = pd.read_csv("yc_combined_startups_data.csv")

# 1. Lead scoring
def calculate_lead_score(row):
    score = 0
    if "B2B" in row['Industries']:
        score += 20
    if "Consumer" in row['Industries']:
        score += 10
    if "AI" in row['Description'].lower():
        score += 10     
    if "Agent" in row['Description'].lower():
        score += 10
    for founder in ['founder1_linkedin','founder2_linkedin','founder3_linkedin']:
        if pd.notnull(row[founder]):
            score += 5
    return score

df['lead_score'] = df.apply(calculate_lead_score, axis=1)

## current lead score is calculated by adding the weights of the factors mentioned above & can be adjusted

# 2. Assign funnel stage
def assign_stage(score):
    if score >= 30:
        return "Demo-Ready"
    elif score >= 25:
        return "SQL (Sales Qualified Lead)"
    else:
        return "MQL (Marketing Qualified Lead)"

df['funnel_stage'] = df['lead_score'].apply(assign_stage)


# 3. Export top leads
df_top = df.sort_values(by='lead_score', ascending=False)
df_top.to_csv("yc_summer2025_top_gtm_leads.csv", index=False)