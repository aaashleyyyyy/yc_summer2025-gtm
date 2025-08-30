# Analyzing YC Summer 2025 Batch for GTM Strategy

---

## Web Scraping

Preface: I would use Clay but I ran out of credits.

Process: I scraped the YC Summer 2025 Batch page to get all the details of each startup and the industries they're in.

outputs:
startups.py --> yc_summer2025_startups.csv
startup-details.py --> yc_summer2025_startups_details.csv
data-cleaning.py --> yc_combined_startups_data.csv

The startups.py scraped the first page which had an overview of each startup and the industries they're in. Then I realized that the founder details were very important, so I scraped each page individually to get all the founders in startup-details.py. I combined all the information in the final yc_combined_startups_data.csv.

## Lead Prioritization

Ideal Customer Profile (ICP): B2B SAAS founder

|  Keyword   |   Column    | Score |
| :--------: | :---------: | :---: |
|   "B2B"    | Industries  |  +20  |
| "Consumer" | Industries  |  +10  |
|    "AI"    | Description |  +10  |
|  "Agent"   | Description |  +10  |

For each additional founder, +5.

Then, each startup was assigned a funnel stage based on their lead scores to help direct resources to better fit companies.

Check out the final table in the yc_summer2025_top_gtm_leads.csv file.
<br>
This is a preliminary project to build great gtm pipelines out of. Thanks for reading <3
