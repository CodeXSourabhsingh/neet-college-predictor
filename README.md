# NEET College Predictor

A mobile-first web app that predicts which government MBBS colleges a NEET aspirant can likely get based on their score, category, and home state — and captures the lead so NEETPrep can follow up.

**Live app:** [URL after deploy]

## What it does

1. Student enters NEET score (0–720), category (General / EWS / OBC / SC / ST), and home state.
2. App converts the score to an estimated All India Rank (AIR) by linear interpolation over 18 published anchor points.
3. After submitting name + 10-digit phone (with consent), the student sees colleges bucketed as:
   - **Safe** — estimated AIR ≤ 85% of the college's closing rank
   - **Moderate** — 85% to 100%
   - **Reach** — 100% to 115%
4. Colleges in the student's home state are flagged with a badge.
5. Every submission is written to a Google Sheet with UTM attribution.

## The lead gate

Results are shown only after the lead form is submitted. This is deliberate — the results are the reward for handing over contact info. Putting the form before the inputs kills conversion; putting it after the results kills lead capture. The gate sits between them.

## Stack

- **Python + Streamlit** — UI and app logic
- **pandas** — loads the two CSVs (colleges, score-to-rank anchors)
- **Google Apps Script + Sheets** — lead storage (no service account, no key file)
- **requests** — POST from Streamlit to the Apps Script webhook

## How it's built

Two files, separate concerns:

- `predictor.py` — pure logic. Two functions: `score_to_air(score)` and `bucket_colleges(air, category, state)`. No UI, no I/O.
- `app.py` — Streamlit wrapper. Inputs, AIR preview, lead form gate, results rendering, WhatsApp share.
- `sheets.py` — Google Sheets writer. POST to Apps Script webhook, optional GET for duplicate phone check.

## Data

Two datasets provided with the assignment:

- `neet_2025_college_cutoffs.csv` — 50 government MBBS colleges, 2025 All India Quota closing ranks by category
- `neet_2025_score_to_rank.csv` — 18 anchor points mapping NEET 2025 score (686 down to 144) to approximate AIR

The data is indicative, prepared for this exercise. Not official MCC data.

## How AI was used

AI was used as a coding partner for syntax and boilerplate — the same way a developer uses Stack Overflow. The architecture, the flow decisions, the bucket boundaries, the lead gate position, and the validation logic were designed by me. Every piece was tested against the assignment's worked example (score 600 → AIR 1,300 → KEM Mumbai / AIIMS Nagpur / AIIMS Raipur).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Where leads are stored

Google Sheet named NEET Leads. Columns: timestamp, name, phone, score, category, state, predicted_air, utm_source, utm_medium, utm_campaign.

## What I cut and why

- OTP verification — out of scope for MVP. Duplicate phone check is a lighter-weight substitute.
- User accounts — unnecessary for a one-shot predictor.
- State-quota counselling — out of scope per the assignment.
- Private / deemed colleges, BDS / AYUSH — out of scope per the assignment.
- SEO — Streamlit apps don't index well; the effort is wasted at this stage.

## Week 2

- OTP verification for real lead quality
- State-quota prediction alongside All India Quota
- WhatsApp share with referral UTM for viral loop
- Admin dashboard: leads by source, conversion rate per channel

## Limitations

- Adult-only data. No adjustment for age or repeat attempts.
- Score-to-AIR interpolation is linear between 18 anchors. Accuracy degrades between sparse anchors.
- Closing ranks are 2025 indicative. Real cutoffs shift year to year.
- Not a substitute for official MCC counselling.

## Author

Sourabh Singh — [LinkedIn](https://linkedin.com/in/sourabh-singh-7b124934) · [GitHub](https://github.com/CodeXSourabhsingh)
