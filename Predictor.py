import pandas as pd

df = pd.read_csv('neet_2025_college_cutoffs.csv')
score_df = pd.read_csv('neet_2025_score_to_rank.csv')

score_df = score_df.sort_values('score', ascending=False).reset_index(drop=True)

CATEGORY_MAP = {
    'General': 'UR',
    'EWS':     'EWS',
    'OBC':     'OBC',
    'SC':      'SC',
    'ST':      'ST',
}

def score_to_air(score):
    if score >= score_df.iloc[0]['score']:
        return int(score_df.iloc[0]['approx_air'])

    if score <= score_df.iloc[-1]['score']:
        return int(score_df.iloc[-1]['approx_air'])

    for i in range(len(score_df) - 1):
        s1 = score_df.iloc[i]['score']
        s2 = score_df.iloc[i + 1]['score']
        if s1 >= score >= s2:
            r1 = score_df.iloc[i]['approx_air']
            r2 = score_df.iloc[i + 1]['approx_air']
            air = r1 + (r2 - r1) * (s1 - score) / (s1 - s2)
            return int(round(air))

    return None  

def bucket_colleges(air, category, state):
    cat = CATEGORY_MAP[category]
    col = f'closing_rank_{cat}'

    safe = []
    moderate = []
    reach = []

    for _, row in df.iterrows():
        closing = row[col]
        ratio = air / closing

        college = {
            'college':          row['college'],
            'city':             row['city'],
            'state':            row['state'],
            'type':             row['type'],
            'closing_rank':     int(closing),
            'home_state_badge': row['state'] == state,
        }

        if ratio <= 0.85:
            safe.append(college)
        elif ratio <= 1.00:
            moderate.append(college)
        elif ratio <= 1.15:
            reach.append(college)
       
    for bucket in (safe, moderate, reach):
        bucket.sort(key=lambda c: c['closing_rank'])

    return safe[:10], moderate[:10], reach[:10]

if __name__ == '__main__':
    print("score 600 →", score_to_air(600))
    print("score 610 →", score_to_air(610))
    print("score 686 →", score_to_air(686))
    print("score 144 →", score_to_air(144))
    print()

    air = score_to_air(600) 
    safe, moderate, reach = bucket_colleges(air, 'General', 'Delhi')
    print("--- Safe ---")
    for c in safe:
        print(f"  {c['college']} (closing {c['closing_rank']})")
    print("--- Moderate ---")
    for c in moderate:
        print(f"  {c['college']} (closing {c['closing_rank']})")
    print("--- Reach ---")
    for c in reach:
        print(f"  {c['college']} (closing {c['closing_rank']})")