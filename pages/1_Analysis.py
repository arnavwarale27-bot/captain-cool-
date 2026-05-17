import streamlit as st
import traceback

try:
    import pandas as pd
    import numpy as np
    HAS_DATA_LIBS = True
except ImportError as e:
    HAS_DATA_LIBS = False
    IMPORT_ERROR = str(e)

# Set page config for a consistent cyberpunk feel
st.set_page_config(page_title="Player Analysis // Captain Cool", page_icon="🏏", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for the Analysis Page
st.markdown("""
<style>
    /* Streamlit App background */
    .stApp {
        background-color: #081425;
        color: #d8e3fb;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Top Custom Navigation Bar matching the main app */
    .custom-nav {
        background: rgba(21, 32, 49, 0.8);
        backdrop-filter: blur(12px);
        padding: 1rem 2rem;
        border-bottom: 1px solid #5b403e;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    .custom-nav h1 {
        color: #bb1522;
        font-family: 'Anton', sans-serif;
        font-style: italic;
        margin: 0;
        font-size: 1.5rem;
        text-shadow: 0 0 10px rgba(255,83,81,0.5);
    }
    .nav-links {
        display: flex;
        gap: 1.5rem;
    }
    .nav-links a {
        color: #d8e3fb;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        cursor: pointer;
    }
    .nav-links a.active {
        color: #e9c400;
        border-bottom: 2px solid #e9c400;
    }
    
    /* Push content down to avoid fixed nav */
    .block-container {
        padding-top: 6rem !important;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #111c2d;
        border: 1px solid #2a3548;
        border-left: 4px solid #e9c400;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    div[data-testid="metric-container"] > div > div > div > p {
        color: #bb1522 !important;
        font-weight: bold;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #ffb3ae !important;
        font-family: 'Anton', sans-serif;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
</style>
<div class="custom-nav">
    <h1>CAPTAIN COOL // NEURAL</h1>
    <div class="nav-links">
        <a href="/" target="_self">Orchestrator</a>
        <a href="/Analysis" target="_self" class="active">Analysis</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("Player Telemetry & Performance Analysis")

if not HAS_DATA_LIBS:
    st.error(f"Missing required data libraries: {IMPORT_ERROR}")
    st.info("Please install pandas and numpy to view this page.")
    st.stop()

# Mock Data Generation for Technical Depth
@st.cache_data
def load_mock_data():
    players = ["Virat Kohli", "Rohit Sharma", "Jasprit Bumrah", "MS Dhoni", "Suryakumar Yadav", "Rashid Khan"]
    roles = ["Top-order Batter", "Opening Batter", "Pace Bowler", "Wicketkeeper Batter", "Middle-order Batter", "Spin Bowler"]
    
    df = pd.DataFrame({
        "Player": players,
        "Role": roles,
        "Overall_Impact_Score": np.random.uniform(75.0, 99.9, size=6).round(1),
        "Tournament_Runs": [450, 380, 25, 150, 410, 80],
        "Tournament_Wickets": [0, 0, 18, 0, 0, 15],
        "Strike_Rate": [135.5, 142.1, 80.0, 160.4, 175.2, 140.0],
        "Economy_Rate": [0, 0, 6.2, 0, 0, 6.8]
    })
    return df

try:
    df = load_mock_data()

    # Layout
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Select Node")
        selected_player = st.selectbox("Player ID", df["Player"].tolist(), label_visibility="collapsed")
        player_data = df[df["Player"] == selected_player].iloc[0]
        
        st.markdown("### Profile Summary")
        st.info(f"**Role:** {player_data['Role']}")
        st.metric("Neural Impact Score", f"{player_data['Overall_Impact_Score']} / 100", delta="Top 5%", delta_color="normal")
        
        st.markdown("---")
        st.markdown("### Core Metrics")
        st.metric("Tournament Runs", int(player_data['Tournament_Runs']))
        st.metric("Strike Rate", f"{player_data['Strike_Rate']}")
        
        if "Bowler" in player_data['Role']:
            st.metric("Tournament Wickets", int(player_data['Tournament_Wickets']))
            st.metric("Economy Rate", f"{player_data['Economy_Rate']}")

    with col2:
        st.subheader(f"Performance Matrices: {selected_player}")
        
        tab1, tab2, tab3 = st.tabs(["Form Progression", "Heatmap (Zone Analysis)", "Technical Variables"])
        
        with tab1:
            st.markdown("**Last 10 Matches Progression (Simulated)**")
            # Generate some volatile time-series data
            progression_data = pd.DataFrame({
                "Match": [f"M{i}" for i in range(1, 11)],
                "Impact Output": np.random.normal(player_data['Overall_Impact_Score'], 10, 10).clip(40, 100),
                "Expected Value": [player_data['Overall_Impact_Score']] * 10
            }).set_index("Match")
            
            st.line_chart(progression_data, color=["#bb1522", "#e9c400"], use_container_width=True)
            
        with tab2:
            st.markdown("**Pitch Zone Efficiency (Strike/Economy Ratio)**")
            # Generate a 2D scatter for "heatmap" proxy
            zones = pd.DataFrame({
                "Length": np.random.uniform(2, 8, 50),
                "Line": np.random.uniform(-1, 1, 50),
                "Efficiency": np.random.uniform(0, 100, 50)
            })
            st.scatter_chart(zones, x="Line", y="Length", size="Efficiency", color="#bb1522", use_container_width=True)
            st.caption("X-Axis: Line (Off to Leg) | Y-Axis: Length (Yorker to Short)")
            
        with tab3:
            st.markdown("**Technical Radar Variables**")
            st.dataframe(
                pd.DataFrame({
                    "Variable": ["Spin Handling", "Pace Handling", "Pressure Index", "Fatigue Resistance", "Clutch Factor"],
                    "Coefficient": np.random.uniform(0.7, 0.99, 5).round(3)
                }),
                use_container_width=True,
                hide_index=True
            )

    # Advanced Data Grid at the bottom
    st.markdown("---")
    st.subheader("Global Player Database [ENCRYPTED]")
    st.dataframe(df, use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Runtime UI Error: {str(e)}")
    st.code(traceback.format_exc())

