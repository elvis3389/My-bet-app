import math

def calculate_poisson_prob(lmbda, k):
    """Calculates probability of exactly k events with mean lmbda."""
    if lmbda <= 0: lmbda = 0.01  # Safety floor
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def goal_market_engine(home_name, away_name, home_lmbda, away_lmbda, line=2.5, odds=None):
    """
    Core Engine for Goal Market Predictions.
    Inputs: Team Names, xG (Lambda), Goal Line (e.g. 2.5), and optional Bookie Odds.
    """
    max_goals = 8  # Sufficient for 99.9% of football outcomes
    
    prob_under = 0.0
    prob_btts_yes = 0.0
    
    # 1. Iterate through the score matrix
    for h in range(max_goals):
        for a in range(max_goals):
            p_score = calculate_poisson_prob(home_lmbda, h) * calculate_poisson_prob(away_lmbda, a)
            
            # Check Under Market
            if (h + a) < line:
                prob_under += p_score
            
            # Check BTTS Yes (Both teams >= 1 goal)
            if h >= 1 and a >= 1:
                prob_btts_yes += p_score

    prob_over = 1 - prob_under
    prob_btts_no = 1 - prob_btts_yes

    # 2. Structure Results for Display
    markets = [
        (f"Over {line}", prob_over, odds.get('over') if odds else None),
        (f"Under {line}", prob_under, odds.get('under') if odds else None),
        ("BTTS (Yes)", prob_btts_yes, odds.get('btts_y') if odds else None),
        ("BTTS (No)", prob_btts_no, odds.get('btts_n') if odds else None),
    ]

    # 3. Formatted Output
    print(f"\n--- Analysis: {home_name} vs {away_name} ---")
    print(f"{'Market':<15} | {'Prob %':<8} | {'Fair Odds':<10} | {'Edge'}")
    print("-" * 55)

    for selection, prob, b_odds in markets:
        fair_odds = 1/prob if prob > 0 else 0
        edge_val = (prob * b_odds - 1) * 100 if b_odds else 0
        edge_str = f"{edge_val:+.1f}%" if b_odds and edge_val > 0 else "---"
        
        print(f"{selection:<15} | {prob*100:>7.1f}% | {fair_odds:>10.2f} | {edge_str}")

# --- HOW TO USE THE MODULE ---
# Example: Replace these with your live data from FotMob/Forebet
current_match = {
    'home': "Team A",
    'away': "Team B",
    'h_xg': 1.65,      # Input Lambda here
    'a_xg': 1.10,      # Input Lambda here
    'line': 2.5,
    'odds': {
        'over': 1.95,  # Input Bookie Odds here
        'under': 1.85,
        'btts_y': 1.70,
        'btts_n': 2.10
    }
}

goal_market_engine(**current_match)
