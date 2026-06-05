import streamlit as st

# --- Enhanced Languages with Flags ---
VOICE_DATA = {
    "Urdu 🇵🇰": "#fbbf24",
    "English 🇺🇸": "#38bdf8",
    "Arabic 🇸🇦": "#34d399",
    "Hindi 🇮🇳": "#f472b6",
    "Spanish 🇪🇸": "#fb923c",
    "Russian 🇷🇺": "#a78bfa",
    "Japanese 🇯🇵": "#f87171",
    "Chinese 🇨🇳": "#60a5fa"
}

st.set_page_config(page_title="VocalForge Studio", layout="wide")

# --- Advanced Metallic-Glass UI ---
css = """
<style>
    .stApp { background-color: #030712 !important; }
    
    /* Dropdown UI Refinement */
    div[data-baseweb="select"] {
        border: 2px solid #334155 !important;
        border-radius: 15px !important;
        background: #0f172a !important;
    }
    
    /* Metallic Glass Capsule Sliders */
    div[data-testid="stSlider"] {
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        padding: 20px 30px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(247, 201, 72, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }
    
    /* Professional Compile Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #d4af37, #aa882c) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        padding: 18px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    h1, h2, h3, label { color: #ffffff !important; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- UI Implementation ---
st.title("🎙️ VocalForge Studio")

col1, col2 = st.columns([1, 1])

with col1:
    selected_lang = st.selectbox("Select Language & Voice", list(VOICE_DATA.keys()))
    
    # Active indicator color
    color = VOICE_DATA[selected_lang]
    st.markdown(f"<h4 style='color: {color};'>Active Voice: {selected_lang}</h4>", unsafe_allow_html=True)
    
    st.slider("Speed", -50, 50, 0)
    st.slider("Pitch", -20, 20, 0)
    
    st.button("🎙 * COMPILE & SYNTHESIZE *")

with col2:
    st.subheader("Script Board")
    st.text_area("Workflow", height=200, placeholder="Enter text here...")

# --- Footer Navigation ---
st.markdown("---")
cols = st.columns(5)
btns = ["Studio", "Privacy", "Terms", "Contact", "Disclaimer"]
for i, name in enumerate(btns):
    cols[i].button(name, key=f"nav_{i}")
