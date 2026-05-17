# 🏏 Captain Cool: Multi-Agent Neural IPL Strategist

![Captain Cool Interface](https://img.shields.io/badge/UI-Cyberpunk%20Dark-red) ![Agent Orchestration](https://img.shields.io/badge/Framework-google.adk-blue) ![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%20%2B%20Tailwind-orange)

An immersive, real-time command console designed to synthesize cricket strategy using a **Multi-Agent Neural Network**. Captain Cool ingests live environmental telemetry and match state to orchestrate a sophisticated debate loop between three specialized LLM agents.

## 🧠 The Agentic Framework
Instead of relying on a single AI prompt, Captain Cool uses **google.adk** to power a 3-Node Neural Debate Loop:
1. **Data Analyst Node (`gemini-2.5-flash`)**: Ingests API telemetry (Live Venue Weather, Dew Risk, Pitch factors) and parses the Match State.
2. **Captain Strategist Node (`gemini-2.5-pro`)**: Synthesizes the data into a high-level Tactical Blueprint (Bowling Lines, Fielding Setups).
3. **Devil's Advocate Node (`gemini-2.5-flash`)**: Vigorously audits the blueprint, finding risks and edge-case vulnerabilities.

The loop culminates in a refined, battle-tested Strategy Directive.

## 🚀 Features
- **Live Telemetry Engine**: Automatically pulls atmospheric data (Temp, Humidity, Dew) via `wttr.in`.
- **Custom Cyberpunk UI**: A highly stylized, dark-mode glassmorphism interface built natively using injected HTML/Tailwind CSS.
- **Deep Analytics Dashboard**: A secondary Data Page featuring Volatility Charts, Pitch Heatmaps, and Simulated Radar Variables.

## ⚙️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/captain-cool.git
cd captain-cool
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
*(Ensure you have installed `streamlit`, `google-adk`, `google-genai`, `pandas`, and `numpy`)*

3. **Configure API Keys**
Create a directory named `.streamlit/` and inside it, create a `secrets.toml` file to securely store your Gemini API Key:
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

4. **Initialize the Console**
```bash
streamlit run app.py
```

## 🛡️ Security
Do not commit your `.streamlit/secrets.toml` file. It is explicitly ignored in `.gitignore` to prevent API key leaks.
# captain-cool-
