import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Pro Market Predictor", layout="wide")
st.title("🎯 Ultimate Market & Team Scorer Module")

# --- Input Section ---
with st.sidebar:
    st.header("Match Data")
    h_name = st.text_input("Home Team", "Home")
    a_name = st.text_input("Away Team", "Away")
    h_exp = st.number_input(f"{h_name} Expected Goals", value=1.5, step=0.1)
    a_exp = st.number_input(f"{a_name} Expected Goals", value=1.2, step=0.1)

def get_detailed_stats(h_l, a_l):
    # Team Goals Probability
    h_probs = [poisson.pmf(i, h_l) for i in range(4)]
    h_probs.append(1 - sum(h_probs)) # 4+ goals
    
    a_probs = [poisson.pmf(i, a_l) for i in range(4)]
    a_probs.append(1 - sum(a_probs)) # 4+ goals
    
    # Match Totals
    over15, over25, over35 = 0, 0, 0
    for h in range(10):
        for a in range(10):
            p = poisson.pmf(h, h_l) * poisson.pmf(a, a_l)
            if h + a > 1.5: over15 += p
            if h + a > 2.5: over25 += p
            if h + a > 3.5: over35 += p
            
    return h_probs, a_probs, [over15, over25, over35]

if st.button("GENERATE FULL MARKET ANALYSIS"):
    h_p, a_p, totals = get_detailed_stats(h_exp, a_exp)
    
    # --- ROW 1: MATCH TOTALS ---
    st.subheader("📊 Match Total Markets")
    t1, t2, t3 = st.columns(3)
    t1.metric("Over 1.5 Goals", f"{round(totals[0]*100)}%")
    t2.metric("Over 2.5 Goals", f"{round(totals[1]*100)}%")
    t3.metric("Over 3.5 Goals", f"{round(totals[2]*100)}%")
    
    st.divider()
    
    # --- ROW 2: TEAM SCORING OPTIONS ---
    st.subheader("⚽ Individual Team Scoring")
    col_h, col_a = st.columns(2)
    
    with col_h:
        st.write(f"**{h_name} Goals**")
        st.write(f"0 Goals: {round(h_p[0]*100)}%")
        st.write(f"1+ Goals: {round((1-h_p[0])*100)}% (Safe Pick)")
        st.write(f"2+ Goals: {round((1-(h_p[0]+h_p[1]))*100)}%")
        
    with col_a:
        st.write(f"**{a_name} Goals**")
        st.write(f"0 Goals: {round(a_p[0]*100)}%")
        st.write(f"1+ Goals: {round((1-a_p[0])*100)}% (Safe Pick)")
        st.write(f"2+ Goals: {round((1-(a_p[0]+a_p[1]))*100)}%")

    st.info("💡 PRO TIP: Look for '1+ Goals' above 80% to build your multi-bet streaks.")
