import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Pro Betting Module", layout="centered")

st.title("⚽ Betting Module")
st.write("Enter match details below:")

# 1. TEAM SECTION
st.subheader("--- Team Stats ---")
h_name = st.text_input("Home Team Name", "Home")
a_name = st.text_input("Away Team Name", "Away")

h_lambda = st.number_input(f"{h_name} Exp. Goals (λ)", value=1.50, step=0.01, format="%.2f")
a_lambda = st.number_input(f"{a_name} Exp. Goals (λ)", value=1.20, step=0.01, format="%.2f")

# 2. MARKET SECTION
st.subheader("--- BetPawa Odds ---")
line = st.selectbox("Goal Line", [1.5, 2.5, 3.5], index=1)
bp_over = st.number_input(f"BetPawa Over {line} Odds", value=1.85, step=0.01)
bp_btts = st.number_input("BetPawa BTTS (Yes) Odds", value=1.75, step=0.01)

# CALCULATION ENGINE
def get_predictions(h_exp, a_exp, goal_line):
    over_p, btts_p = 0, 0
    for h in range(10):
        for a in range(10):
            prob = poisson.pmf(h, h_exp) * poisson.pmf(a, a_exp)
            if h + a > goal_line: over_p += prob
            if h > 0 and a > 0: btts_p += prob
    return over_p, btts_p

if st.button("RUN ANALYSIS"):
    over_p, btts_p = get_predictions(h_lambda, a_lambda, line)
    
    st.markdown("---")
    
    # Results Display
    st.write(f"### Results for {h_name} vs {a_name}")
    
    # Over/Under Result
    o_fair = 1/over_p
    o_edge = (over_p - (1/bp_over)) * 100
    st.info(f"**Over {line}:** {round(over_p*100,1)}% (Fair Odds: {round(o_fair,2)})")
    if o_edge > 5: st.success(f"🔥 VALUE FOUND: {round(o_edge,1)}% Edge")

    # BTTS Result
    b_fair = 1/btts_p
    b_edge = (btts_p - (1/bp_btts)) * 100
    st.info(f"**BTTS (Yes):** {round(btts_p*100,1)}% (Fair Odds: {round(b_fair,2)})")
    if b_edge > 5: st.success(f"🔥 VALUE FOUND: {round(b_edge,1)}% Edge")
