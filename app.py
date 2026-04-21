import math

def poisson_prob(lmbda, k):
    """Calculates probability of exactly k goals."""
    if lmbda <= 0: lmbda = 0.01  # Safety Floor for zero-scoring teams
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def goal_market_module(home_xg, away_xg, bookie_odds=None):
    # 1. Generate Score Matrix (Probabilities for scores 0-0 to 5-5)
    max_goals = 6
    matrix = [[0] * max_goals for _ in range(max_goals)]
    
    prob_btts_yes = 0
    prob_under_1_5 = 0
    prob_under_2_5 = 0
    
    print(f"--- Goal Market Analysis (Home xG: {home_xg} | Away xG: {away_xg}) ---")
    
    for h in range(max_goals):
        for a in range(max_goals):
            prob = poisson_prob(home_xg, h) * poisson_prob(away_xg, a)
            matrix[h][a] = prob
            
            # Cumulative Market Logic
            if h > 0 and a > 0:
                prob_btts_yes += prob
            if h + a < 1.5:
                prob_under_1_5 += prob
            if h + a < 2.5:
                prob_under_2_5 += prob

    # 2. Market Output Table
    markets = [
        ("Over 1.5", 1 - prob_under_1_5, bookie_odds.get('o15') if bookie_odds else None),
        ("Over 2.5", 1 - prob_under_2_5, bookie_odds.get('o25') if bookie_odds else None),
        ("BTTS (Yes)", prob_btts_yes, bookie_odds.get('btts_y') if bookie_odds else None),
        ("BTTS (No)", 1 - prob_btts_yes, bookie_odds.get('btts_n') if bookie_odds else None)
    ]

    print(f"{'Selection':<12} | {'Prob %':<8} | {'Fair Odds':<10} | {'Edge'}")
    print("-" * 50)
    
    for name, p, b_odds in markets:
        fair = 1/p if p > 0 else 0
        edge = (p * b_odds - 1) * 100 if b_odds else 0
        edge_str = f"{edge:.1f}%" if edge > 0 else "---"
        print(f"{name:<12} | {p*100:>6.1f}% | {fair:>10.2f} | {edge_str}")

# --- EXAMPLE USAGE ---
# Let's say Home xG is 1.4 and Away xG is 0.8
# You can also input current bookie odds to see if there's an edge
my_odds = {'o15': 1.45, 'o25': 2.10, 'btts_y': 1.95, 'btts_n': 1.80}
goal_market_module(1.4, 0.8, bookie_odds=my_odds)
