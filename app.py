import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Pro Betting Module", page_icon="⚽")
st.title("⚽ Goals & BTTS Prediction Module")

col1, col2 = st.columns(2)

with col1:
    st.header("1. Match Stats")
    h_lambda = st.number_input("Home Exp. Goals (λ)", value=1.5, step=0.1)
    a_lambda = st.number_input("Away Exp. Goals (λ)", value=1.2, step=0.1)
    line = st.selectbox("Goal Line", [1.5, 2.5, 3.5], index=1)

with col2:
    st.header("2. BetPawa Odds")
    bp_over = st.number_input(f"Over {line} Odds", value=1.85)
    bp_btts = st.number_input("BTTS (Yes) Odds", value=1.70)

def get_predictions(h_exp, a_exp, goal_line):
    over_p = 0
    btts_p = 0
    for h in range(10):
        for a in range(10):
            prob = poisson.pmf(h, h_exp) * poisson.pmf(a, a_exp)
            # Goals logic
            if h + a > goal_line:
                over_p += prob
            # BTTS logic
            if h > 0 and a > 0:
                btts_p += prob
    return over_p, btts_p

if st.button("RUN DUAL-MARKET ANALYSIS"):
    over_p, btts_p = get_predictions(h_lambda, a_lambda, line)
    
    st.divider()
    res1, res2 = st.columns(2)
    
    # Goals Result
    over_edge = (over_p - (1/bp_over)) * 100
    res1.subheader(f"Over {line} Goals")
    res1.metric("Prob", f"{round(over_p*100, 1)}%")
    res1.write(f"Fair Odds: {round(1/over_p, 2)}")
    if over_edge > 5: res1.success(f"VALUE: {round(over_edge, 1)}% Edge")
    
    # BTTS Result
    btts_edge = (btts_p - (1/bp_btts)) * 100
    res2.subheader("BTTS (Yes)")
    res2.metric("Prob", f"{round(btts_p*100, 1)}%")
    res2.write(f"Fair Odds: {round(1/btts_p, 2)}")
    if btts_edge > 5: res2.success(f"VALUE: {round(btts_edge, 1)}% Edge")
