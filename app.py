import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Dual-Market Betting Pro", layout="centered")

st.title("⚽ Goals & BTTS Prediction Module")
st.write("Professional analysis for BetPawa markets.")

# --- INPUT SECTION ---
st.subheader("--- Match Parameters ---")
h_name = st.text_input("Home Team", "Home Team")
a_name = st.text_input("Away Team", "Away Team")

col_a, col_b = st.columns(2)
h_lambda = col_a.number_input(f"{h_name} Exp. Goals (λ)", value=1.50, step=0.01)
a_lambda = col_b.number_input(f"{a_name} Exp. Goals (λ)", value=1.20, step=0.01)

st.subheader("--- BetPawa Market Odds ---")
line = st.selectbox("Goal Line", [1.5, 2.5, 3.5], index=1)
odd_over = st.number_input(f"BetPawa Over {line} Odds", value=1.85)
odd_under = st.number_input(f"BetPawa Under {line} Odds", value=1.85)

st.divider()
odd_btts_yes = st.number_input("BetPawa BTTS (Yes) Odds", value=1.75)
odd_btts_no = st.number_input("BetPawa BTTS (No) Odds", value=1.95)

# --- THE CALCULATOR ---
def run_math(h_exp, a_exp, goal_line):
    over_p, under_p, btts_y_p = 0, 0, 0
    for h in range(12): 
        for a in range(12):
            prob = poisson.pmf(h, h_exp) * poisson.pmf(a, a_exp)
            # Goals logic
            if h + a > goal_line: over_p += prob
            else: under_p += prob
            # BTTS logic (Both must be > 0)
            if h > 0 and a > 0: btts_y_p += prob
            
    btts_n_p = 1 - btts_y_p
    return over_p, under_p, btts_y_p, btts_n_p

if st.button("RUN FULL ANALYSIS"):
    ov, un, b_y, b_n = run_math(h_lambda, a_lambda, line)
    
    # 1. GOALS RESULTS
    st.markdown("### 📊 Market: Total Goals")
    c1, c2 = st.columns(2)
    
    for p, odd, label, col in [(ov, odd_over, f"OVER {line}", c1), (un, odd_under, f"UNDER {line}", c2)]:
        edge = (p - (1/odd)) * 100
        col.metric(label, f"{round(p*100, 1)}%")
        col.write(f"Fair Odds: {round(1/p, 2)}")
        if edge > 5: col.success(f"VALUE: {round(edge, 1)}% Edge")

    st.divider()

    # 2. BTTS RESULTS
    st.markdown("### 📊 Market: Both Teams to Score")
    c3, c4 = st.columns(2)
    
    for p, odd, label, col in [(b_y, odd_btts_yes, "BTTS (Yes)", c3), (b_n, odd_btts_no, "BTTS (No)", c4)]:
        edge = (p - (1/odd)) * 100
        col.metric(label, f"{round(p*100, 1)}%")
        col.write(f"Fair Odds: {round(1/p, 2)}")
        if edge > 5: col.success(f"VALUE: {round(edge, 1)}% Edge")
