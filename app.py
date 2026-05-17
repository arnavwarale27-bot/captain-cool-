import os
import time
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List
import requests

import streamlit as st
import streamlit.components.v1 as components

try:
    from google.adk import Agent
    from google.adk.tools import Tool
except ImportError:
    pass

# --- ENTERPRISE CONFIGURATION & LOGGING ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [CORE_ENGINE] - %(levelname)s - %(message)s")
logger = logging.getLogger("AgenticPipeline")

st.set_page_config(page_title="Captain Cool", layout="wide", initial_sidebar_state="collapsed")
# Securely load API Key from Streamlit Secrets (prevent GitHub exposure)
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
elif not os.environ.get("GEMINI_API_KEY"):
    logger.warning("No GEMINI_API_KEY found in environment or secrets.")

# --- DOMAIN MODELS ---
@dataclass
class MatchTelemetry:
    venue: str
    runs: int
    wickets: int
    raw_weather_data: Optional[str] = field(default=None)

@dataclass
class AgentSynthesis:
    analyst_report: str
    captain_strategy: str
    advocate_dissent: str
    final_blueprint: str

# --- TELEMETRY SUBSYSTEM ---
class TelemetryEngine:
    """Handles external API integrations and real-time environment data extraction."""
    @staticmethod
    def fetch_weather(venue: str) -> str:
        logger.info(f"Initiating atmospheric telemetry fetch for {venue}")
        try:
            city = venue.split(',')[1].strip() if ',' in venue else venue.split(' ')[0]
            url = f"https://wttr.in/{city}?format=j1"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                humidity = int(data['current_condition'][0]['humidity'])
                temp = data['current_condition'][0]['temp_C']
                dew_risk = "CRITICAL" if humidity > 75 else ("ELEVATED" if humidity > 60 else "LOW")
                logger.info(f"Telemetry acquired: {temp}C, {humidity}% Hum. Risk: {dew_risk}")
                return f"Atmospheric Data: {temp}°C, Humidity: {humidity}%. Dew Risk: {dew_risk}. Factor this into the ball grip and spin potential."
        except Exception as e:
            logger.error(f"Telemetry failure: {str(e)}")
        return "Telemetry unavailable. Assume high dew risk (standard night match conditions)."

# --- MULTI-AGENT ORCHESTRATOR ---
class AgenticDebateFramework:
    """
    Advanced Multi-Agent orchestration framework utilizing google.adk.
    Implements a sequential reasoning loop: Analyze -> Strategize -> Critique -> Refine.
    """
    def __init__(self, telemetry: MatchTelemetry):
        self.telemetry = telemetry
        self.weather_tool = Tool.from_function(TelemetryEngine.fetch_weather, name="fetch_venue_weather", description="Fetches live weather and calculates Dew Risk.")

    def _simulated_fallback(self) -> AgentSynthesis:
        logger.warning("Using mock framework synthesis. API key not detected or ADK unavailable.")
        time.sleep(1.5)
        return AgentSynthesis(
            analyst_report="Based on historical venue data at this stadium, the pitch flattens under lights. Dew risk is critical. Spinners will struggle to grip the ball.",
            captain_strategy="Understood. We will rely on our pacers to bowl heavy off-cutters and wide yorkers to take the pace off. Spinners will be held back.",
            advocate_dissent="CRITICAL FLAW: Taking the pace off with a wet ball is highly risky; full tosses are likely. We must attack the stumps with hard lengths instead.",
            final_blueprint="**FINAL DIRECTIVE:**\\n1. Attack stumps with hard lengths initially.\\n2. Keep a deep square leg for the hook shot.\\n3. Only use wide yorkers if the ball is dry."
        )

    def execute_neural_loop(self) -> AgentSynthesis:
        if os.environ.get("GEMINI_API_KEY") == "PASTE_YOUR_API_KEY_HERE" or not os.environ.get("GEMINI_API_KEY"):
            return self._simulated_fallback()
            
        try:
            logger.info("Initializing Agent Network...")
            # 1. Data Analyst Node
            analyst = Agent(name="Data_Analyst", model="gemini-2.5-flash", instructions="You are a data-driven cricket analyst. You speak technically, analyzing pitch, weather, and score. Be concise.", tools=[self.weather_tool])
            # 2. Captain Strategist Node
            captain = Agent(name="Captain_Strategist", model="gemini-2.5-pro", instructions="You are the tactical mastermind. Create a bowling/fielding plan based on the analyst's report.")
            # 3. Devil's Advocate Node
            devil = Agent(name="Devils_Advocate", model="gemini-2.5-flash", instructions="You are the Devil's Advocate. Your job is to strictly criticize the captain's plan, pointing out massive vulnerabilities.")

            state_prompt = f"Venue: {self.telemetry.venue} | Score: {self.telemetry.runs}/{self.telemetry.wickets}."
            
            # Step 1: Analysis
            logger.info("Executing Node 1: Analyst")
            analyst_out = analyst.run(f"Provide atmospheric and pitch analysis for: {state_prompt}")
            
            # Step 2: Strategy
            logger.info("Executing Node 2: Captain")
            capt_initial = captain.run(f"Based on this analyst report, what is the initial bowling and fielding strategy?\\nReport: {analyst_out.text}")
            
            # Step 3: Dissent
            logger.info("Executing Node 3: Advocate")
            dissent = devil.run(f"Critique this strategy severely. Find the flaws.\\nStrategy: {capt_initial.text}")
            
            # Step 4: Final Synthesis
            logger.info("Executing Final Node: Synthesis")
            blueprint = captain.run(f"Refine your strategy by aggressively incorporating or defending against this dissent.\\nDissent: {dissent.text}")
            
            return AgentSynthesis(
                analyst_report=analyst_out.text,
                captain_strategy=capt_initial.text,
                advocate_dissent=dissent.text,
                final_blueprint=blueprint.text
            )
        except Exception as e:
            logger.error(f"Orchestrator crashed: {str(e)}")
            return self._simulated_fallback()

# --- PRESENTATION LAYER ---
def format_chat_message(role: str, content: str, color_class: str, icon: str) -> str:
    content_html = content.replace('\\n', '<br>').replace('\n', '<br>')
    return f'''
    <div class="flex items-start gap-4 transform transition-all duration-500 hover:translate-x-2">
        <div class="w-10 h-10 rounded-lg bg-surface-container-high border border-{color_class}/50 flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(var(--{color_class}-rgb),0.2)]">
            <span class="material-symbols-outlined text-{color_class} text-xl">{icon}</span>
        </div>
        <div class="flex-1">
            <p class="text-[11px] font-bold tracking-widest text-{color_class} mb-1">{role} // SYS.NODE</p>
            <div class="bg-surface-container/80 backdrop-blur-md p-4 rounded-r-xl rounded-bl-xl border border-outline-variant/30 text-on-surface shadow-lg text-sm leading-relaxed">
                {content_html}
            </div>
        </div>
    </div>
    '''

def render_application():
    try:
        with open("index.html", "r") as f:
            html_content = f.read()
    except Exception:
        st.error("Fatal UI Error: index.html missing.")
        st.stop()

    if "trigger" in st.query_params:
        v_venue = st.query_params.get("venue", "Wankhede Stadium, Mumbai")
        v_runs = st.query_params.get("runs", "142")
        v_wickets = st.query_params.get("wickets", "4")
        
        # Build telemetry
        telemetry = MatchTelemetry(venue=v_venue, runs=int(v_runs), wickets=int(v_wickets))
        
        # Execute enterprise framework
        engine = AgenticDebateFramework(telemetry)
        synthesis = engine.execute_neural_loop()
        
        # Build UI Injection
        debate_html = ""
        debate_html += format_chat_message("DATA ANALYST", synthesis.analyst_report, "blue-400", "analytics")
        debate_html += format_chat_message("CAPTAIN STRATEGIST", synthesis.captain_strategy, "yellow-500", "psychology")
        debate_html += format_chat_message("DEVIL'S ADVOCATE", synthesis.advocate_dissent, "red-500", "warning")
        
        # Inject state
        html_content = html_content.replace(f'<option value="{v_venue}">{v_venue}</option>', f'<option value="{v_venue}" selected>{v_venue}</option>')
        html_content = html_content.replace('value="142"', f'value="{v_runs}"')
        html_content = html_content.replace('value="4"', f'value="{v_wickets}"')
        
        # Inject debate
        html_content = html_content.replace('<!--INJECT_DEBATE-->', debate_html)
        
        # Inject final blueprint
        bp_html = f'<div class="text-tertiary font-mono text-xs">{synthesis.final_blueprint.replace(chr(10), "<br>")}</div>'
        html_content = html_content.replace('<!--INJECT_BLUEPRINT-->\nWaiting for Matrix Trigger...', bp_html)
        html_content = html_content.replace('<!--INJECT_BLUEPRINT-->\\nWaiting for Matrix Trigger...', bp_html)

    # UI Reset for Streamlit - Fullscreen Mode
    st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        header[data-testid="stHeader"] {
            display: none !important; /* Hides the white Streamlit top bar */
        }
        div[data-testid="stToolbar"] {
            display: none !important;
        }
        iframe {
            height: 100vh !important;
            width: 100% !important;
            border: none;
        }
    </style>
    """, unsafe_allow_html=True)
    components.html(html_content, height=900, scrolling=False)

if __name__ == "__main__":
    render_application()
