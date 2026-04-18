import streamlit as st
from scipy.stats import poisson

# App Header
st.set_page_config(page_title="Betting Module Pro", page_icon="⚽")
st.title("⚽ Over/Under Prediction Module")
st.markdown("Automated Poisson Distribution Engine for BetPawa Markets")

# Layout Columns
col1, col2 = st.columns(2)

with col1:
    st.header("1. Team Stats (λ)")
    home_name = st.text_input("Home Team", "Home Team")
    away_name = st.text_input("Away Team", "Away Team")
    h_lambda = st.number_input(f"{home_name} Exp. Goals", value=1.5, step=0.1)
    a_lambda = st.number_input(f"{away_name} Exp. Goals", value=1.2, step=0.1)

with col2:
    st.header("2. BetPawa Odds")
    line = st.selectbox("Goal Line", [1.5, 2.5, 3.5], index=1)
    bp_over = st.number_input(f"BetPawa Over {line} Odds", value=1.85)
    bp_under = st.number_input(f"BetPawa Under {line} Odds", value=1.85)

# Calculation Engine
def get_probs(h_exp, a_exp, goal_line):
    under_p = 0
    for h in range(10):
        for a in range(10):
            if h + a < goal_line:
                under_p += poisson.pmf(h, h_exp) * poisson.pmf(a, a_exp)
    return 1 - under_p, under_p

if st.button("RUN PREDICTION"):
    over_p, under_p = get_probs(h_lambda, a_lambda, line)
    fair_over = 1 / over_p
    edge = (over_p - (1/bp_over)) * 100

    st.divider()
    res1, res2, res3 = st.columns(3)
    res1.metric("Over Probability", f"{round(over_p*100, 1)}%")
    res2.metric("Fair Market Odds", f"{round(fair_over, 2)}")
    
    if edge > 5:
        res3.success(f"VALUE: {round(edge,1)}% Edge")
    elif edge > 0:
        res3.warning(f"Slight Value: {round(edge,1)}%")
    else:
        res3.error("NO VALUE")
