import streamlit as st
import asyncio

# --- Configuration & Language Data with Flag & Color Mapping ---
# Imran Bhai, har language ka apna flag aur specific vibrant color map kar diya hai.
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

# --- Dynamic Cinematic Backgrounds ---
IMAGES = [
    "https://images.unsplash.com/photo-1516280440614-37939bbacd6a",
    "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04",
    "https://images.unsplash.com/photo-1478737270239-2f02b77fc618",
    "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0",
    "https://images.unsplash.com/photo-1484755560693-a4074577af3a",
    "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4",
    "https://images.unsplash.com/photo-1514525253161-7a46d19cd819",
    "https://images.unsplash.com/photo-1459749411175-04bf5292ceea",
    "https://images.unsplash.com/photo-1465847899084-d164df4dedc6",
    "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad"
]

st.set_page_config(page_title="VocalForge Studio", layout="wide")

# --- Refined CSS Engine ---
css = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(3, 7, 22, 0.9), rgba(3, 7, 22, 0.9)), url('{IMAGES[0]}');
        background-size: cover;
        animation: bgChange 600s infinite;
    }}
    @keyframes bgChange {{
        {" ".join([f"{i*10}% {{ background-image: linear-gradient(rgba(3, 7, 22, 0.9), rgba(3, 7, 22, 0.9)), url('{img}'); }}" for i, img in enumerate(IMAGES)])}
    }}
    /* Metallic Capsule Sliders */
    div[data-testid="stSlider"] {{
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        padding: 20px 30px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(247, 201, 72, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }}
    /* Metallic Compile Button */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(180deg, #d4af37, #aa882c) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: none !important;
    }}
    h1, h2, label {{ color: #ffffff !important; }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- UI Implementation ---
st.title("🎙️ VocalForge Studio")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Voice Settings")
    sel_lang = st.selectbox("Select Language & Voice", list(VOICE_DATA.keys()))
    
    # Dynamic Color Header based on Language
    color = VOICE_DATA[sel_lang]["color"]
    st.markdown(f"<h4 style='color: {color};'>Selected: {sel_lang}</h4>", unsafe_allow_html=True)
    
    speed = st.slider("Speed", -50, 50, 0)
    pitch = st.slider("Pitch", -20, 20, 0)
    
    if st.button("🎙 * COMPILE & SYNTHESIZE AUDIO *"):
        st.success(f"Synthesizing in {sel_lang}...")

with col2:
    st.subheader("Script Board")
    input_text = st.text_area("Workflow", height=200, placeholder="Enter your sequence narrative...")

# --- Footer ---
st.markdown("---")
cols = st.columns(5)
btns = ["Studio", "Privacy", "Terms", "Contact", "Disclaimer"]
for i, name in enumerate(btns):
    cols[i].button(name, key=f"nav_{i}")
