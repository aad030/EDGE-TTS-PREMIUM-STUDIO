import asyncio
import edge_tts
import streamlit as st
import os
import re
import zipfile
import io

# --- Expanded Language/Voice List ---
VOICES = {
    "Asad (Urdu) 🇵🇰": "ur-PK-AsadNeural",
    "Uzma (Urdu) 🇵🇰": "ur-PK-UzmaNeural",
    "Christopher (Eng) 🇺🇸": "en-US-ChristopherNeural",
    "Ava (English) 🇺🇸": "en-US-AvaNeural",
    "Hamed (Arabic) 🇸🇦": "ar-SA-HamedNeural",
    "Sana (Arabic) 🇸🇦": "ar-SA-SanaNeural",
    "Madhur (Hindi) 🇮🇳": "hi-IN-MadhurNeural",
    "Swara (Hindi) 🇮🇳": "hi-IN-SwaraNeural",
    "Elena (Spanish) 🇪🇸": "es-ES-ElenaNeural",
    "Alvaro (Spanish) 🇪🇸": "es-ES-AlvaroNeural",
    "Katya (Russian) 🇷🇺": "ru-RU-KatyaNeural",
    "Dmitry (Russian) 🇷🇺": "ru-RU-DmitryNeural",
    "Nanami (Japanese) 🇯🇵": "ja-JP-NanamiNeural",
    "Keita (Japanese) 🇯🇵": "ja-JP-KeitaNeural",
    "Xiaoxiao (Chinese) 🇨🇳": "zh-CN-XiaoxiaoNeural",
    "Yunxi (Chinese) 🇨🇳": "zh-CN-YunxiNeural"
}

# --- Background Image Pool ---
images = [
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

# --- CSS Engine ---
css = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(3, 7, 22, 0.9), rgba(3, 7, 22, 0.9)), url('{images[0]}');
        background-size: cover;
        animation: bgChange 600s infinite;
    }}
    @keyframes bgChange {{
        {" ".join([f"{i*10}% {{ background-image: linear-gradient(rgba(3, 7, 22, 0.9), rgba(3, 7, 22, 0.9)), url('{img}'); }}" for i, img in enumerate(images)])}
    }}
    div[data-testid="stSlider"] {{
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        padding: 20px 30px !important;
        border-radius: 50px !important;
        border: 1px solid rgba(247, 201, 72, 0.3) !important;
    }}
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(180deg, #d4af37, #aa882c) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        border: none !important;
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("🎙️ VocalForge Studio")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Voice Settings")
    sel_voice = st.selectbox("Select Voice", list(VOICES.keys()))
    speed = st.slider("Speed", -50, 50, -29)
    pitch = st.slider("Pitch", -20, 20, -9)
    if st.button("🎙 * COMPILE & SYNTHESIZE AUDIO *"):
        st.success("Synthesis initiated...")

with col2:
    st.subheader("Script Board")
    input_text = st.text_area("Workflow", height=200, placeholder="Enter your sequence narrative...")

st.markdown("---")
cols = st.columns(5)
btns = ["Studio", "Privacy", "Terms", "Contact", "Disclaimer"]
for i, name in enumerate(btns):
    cols[i].button(name, key=f"nav_{i}")
