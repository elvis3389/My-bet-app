import streamlit as st
from scipy.stats import poisson

st.set_page_config(page_title="Streak Builder Pro", layout="wide")
st.title("🚀 Multi-Bet Streak Module")

def calculate_probs(h_exp, a_exp, line):
    ov, un, b_y = 0, 0, 0
    for h in range(10):
        for a in range(10):
            p = poisson.pmf(h, h_exp) * poisson.pmf(a, a_exp)
            if h + a > line: ov += p
            else: un += p
            if h > 0 and a > 0: b_y += p
    return ov, un, b_y, 1-b_y

# Sidebar for Slip Math
st.sidebar.header("Slip Summary")
total_odds = st.sidebar.number_input("Target Total Odds", value=1.0)
stake = st.sidebar.number_input("Stake (UGX)", value=100000)
st.sidebar.write(f"**Potential Payout:** {round(total_odds * stake, 2)} UGX")

# Main Input Area
num_games = st.slider("How many games in your streak?", 2, 6, 4)
all_data = []

for i in range(num_games):
    with st.expander(f"Game {i+1} Setup", expanded=True):
        c1, c2, c3 = st.columns(3)
        h_name = c1.text_input(f"Home {i+1}", f"Team A")
        h_l = c2.number_input(f"{h_name} λ", value=1.5, key=f"h{i}")
        a_l = c3.number_input(f"Away {i+1} λ", value=1.2, key=f"a{i}")
        
        ov, un, by, bn = calculate_probs(h_l, a_l, 2.5)
        
        # Display the "Safe" Picks
        res1, res2, res3 = st.columns(3)
        res1.metric("Over 2.5", f"{round(ov*100)}%")
        res2.metric("Under 2.5", f"{round(un*100)}%")
        res3.metric("BTTS (Yes)", f"{round(by*100)}%")
        
        # Highlight the Strongest Pick
        picks = {"Over 2.5": ov, "Under 2.5": un, "BTTS (Yes)": by, "BTTS (No)": bn}
        best_bet = max(picks, key=picks.get)
        st.success(f"Best Stat Pick: **{best_bet}** ({round(picks[best_bet]*100)}% Confidence)")
