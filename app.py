import streamlit as st

# --- Config & Data ---
VOICE_DATA = {
    "Urdu 🇵🇰": {"color": "#fbbf24"},
    "English 🇺🇸": {"color": "#38bdf8"},
    "Arabic 🇸🇦": {"color": "#34d399"},
    "Hindi 🇮🇳": {"color": "#f472b6"},
    "Spanish 🇪🇸": {"color": "#fb923c"},
    "Russian 🇷🇺": {"color": "#a78bfa"},
    "Japanese 🇯🇵": {"color": "#f87171"},
    "Chinese 🇨🇳": {"color": "#60a5fa"}
}

st.set_page_config(page_title="VocalForge Studio", layout="wide")

# --- Mobile Optimized CSS Engine ---
css = """
<style>
    .stApp { background-color: #030712 !important; }
    
    /* Responsive Layout Fixes */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
        /* Make nav buttons compact on mobile */
        div[data-testid="stHorizontalBlock"] button { padding: 5px !important; font-size: 12px !important; }
    }
    
    /* Metallic Capsule Sliders */
    div[data-testid="stSlider"] {
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        padding: 15px 20px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(247, 201, 72, 0.3) !important;
        margin-bottom: 15px !important;
    }
    
    /* Metallic Compile Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #d4af37, #aa882c) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        border: none !important;
    }
    h1, h2, label { color: #ffffff !important; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- UI Implementation ---
st.title("🎙️ VocalForge Studio")

# Use single column for mobile stacking, two columns for desktop
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Voice Settings")
    sel_lang = st.selectbox("Select Language & Voice", list(VOICE_DATA.keys()))
    color = VOICE_DATA[sel_lang]["color"]
    st.markdown(f"<h4 style='color: {color};'>Selected: {sel_lang}</h4>", unsafe_allow_html=True)
    speed = st.slider("Speed", -50, 50, 0)
    pitch = st.slider("Pitch", -20, 20, 0)
    if st.button("🎙 * COMPILE & SYNTHESIZE *"):
        st.success("Synthesizing...")

with col2:
    st.subheader("Script Board")
    input_text = st.text_area("Workflow", height=200, placeholder="Enter narrative...")

# --- Mobile Friendly Footer Nav ---
st.markdown("---")
# Using a 5-column layout that naturally wraps on very small screens
cols = st.columns(5)
btns = ["Studio", "Privacy", "Terms", "Contact", "Disclaimer"]
for i, name in enumerate(btns):
    cols[i].button(name, key=f"nav_{i}")
