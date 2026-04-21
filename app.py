import streamlit as st
from scipy.stats import poisson

st.title("⚽ Day One: Poisson Goal Predictor")

# 1. THE INPUTS
h_exp = st.number_input("Home Expected Goals (λ)", value=1.50)
a_exp = st.number_input("Away Expected Goals (λ)", value=1.20)

# 2. THE MATH ENGINE
def get_probabilities(h_lambda, a_lambda):
    over_25 = 0
    under_25 = 0
    btts_yes = 0
    
    for h in range(10): # Home goals 0-9
        for a in range(10): # Away goals 0-9
            # Probability of this specific score (e.g., 2-1)
            prob = poisson.pmf(h, h_lambda) * poisson.pmf(a, a_lambda)
            
            # Check Match Totals
            if h + a > 2.5:
                over_25 += prob
            else:
                under_25 += prob
                
            # Check BTTS
            if h > 0 and a > 0:
                btts_yes += prob
                
    return over_25, under_25, btts_yes

# 3. THE OUTPUTS
if st.button("Calculate Day One Odds"):
    ov, un, btts = get_probabilities(h_exp, a_exp)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Over 2.5", f"{round(ov*100, 1)}%")
    col2.metric("Under 2.5", f"{round(un*100, 1)}%")
    col3.metric("BTTS (Yes)", f"{round(btts*100, 1)}%")
