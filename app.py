import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Pro-Adjusted Predictor", layout="centered")

st.title("🛡️ Game 5: Pro-Adjusted Module")
st.write("Applying defensive weighting to beat the averages.")

# --- INPUT SECTION ---
st.subheader("1. Raw Stats & Team Info")
h_name = st.text_input("Home Team", "Arsenal")
a_name = st.text_input("Away Team", "Chelsea")

col1, col2 = st.columns(2)
h_raw = col1.number_input(f"{h_name} Raw λ (Avg)", value=1.50, step=0.01)
a_raw = col2.number_input(f"{a_name} Raw λ (Avg)", value=1.20, step=0.01)

st.subheader("2. Pro Adjustments")
st.info("💡 Reduce Away λ if the Home team has a 'Fortress' defense.")
adj_h = st.slider(f"{h_name} Adjustment (%)", 50, 150, 100) / 100
adj_a = st.slider(f"{a_name} Adjustment (%)", 50, 150, 100) / 100

# Final Adjusted Lambdas
h_lambda = h_raw * adj_h
a_lambda = a_raw * adj_a

st.write(f"**Final Applied λ:** {h_name}: `{round(h_lambda, 2)}` | {a_name}: `{round(a_lambda, 2)}`")

st.subheader("3. BetPawa Market Odds")
line = st.selectbox("Goal Line", [1.5, 2.5, 3.5], index=1)
odd_over = st.number_input(f"BetPawa Over {line} Odds", value=1.90)
odd_under = st.number_input(f"BetPawa Under {line} Odds", value=1.90)
odd_btts_y = st.number_input("BTTS (Yes) Odds", value=1.80)
odd_btts_n = st.number_input("BTTS (No) Odds", value=1.90)

# --- THE CALCULATOR ENGINE ---
def run_analysis(h_l, a_l, g_line):
    ov, un, b_y = 0, 0, 0
    for h in range(12): 
        for a in range(12):
            # Safe Poisson for 0.00 inputs
            p_h = poisson.pmf(h, h_l) if h_l > 0 else (1.0 if h == 0 else 0.0)
            p_a = poisson.pmf(a, a_l) if a_l > 0 else (1.0 if a == 0 else 0.0)
            prob = p_h * p_a
            
            if h + a > g_line: ov += prob
            else: un += prob
            if h > 0 and a > 0: b_y += prob
            
    return ov, un, b_y, 1-b_y

if st.button("RUN ADJUSTED ANALYSIS"):
    ov_p, un_p, by_p, bn_p = run_analysis(h_lambda, a_lambda, line)
    
    # --- DISPLAY RESULTS ---
    res_col1, res_col2 = st.columns(2)
    
    # Total Goals
    with res_col1:
        st.markdown(f"### Goals (Line {line})")
        for p, odd, lbl in [(ov_p, odd_over, "OVER"), (un_p, odd_under, "UNDER")]:
            edge = (p - (1/odd)) * 100
            st.metric(f"{lbl} {line}", f"{round(p*100, 1)}%")
            if edge > 5: st.success(f"VALUE: {round(edge, 1)}% Edge")

    # BTTS
    with res_col2:
        st.markdown("### BTTS Market")
        for p, odd, lbl in [(by_p, odd_btts_y, "Yes"), (bn_p, odd_btts_n, "No")]:
            edge = (p - (1/odd)) * 100
            st.metric(f"BTTS {lbl}", f"{round(p*100, 1)}%")
            if edge > 5: st.success(f"VALUE: {round(edge, 1)}% Edge")
