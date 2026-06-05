import asyncio
import edge_tts
import streamlit as st
import os
import re
import zipfile
import io

OUTPUT_DIR = "output_voices"

# Premium Voices Mapping (Global Multilingual Tier-1 Models)
VOICES = {
    "Asad (Urdu - Male) 🇵🇰": "ur-PK-AsadNeural",
    "Uzma (Urdu - Female) 🇵🇰": "ur-PK-UzmaNeural",
    "Christopher (English - Male) 🇺🇸": "en-US-ChristopherNeural",
    "Ava (English - Female) 🇺🇸": "en-US-AvaNeural",
    "Hamed (Arabic - Male) 🇸🇦": "ar-SA-HamedNeural",
    "Sana (Arabic - Female) 🇸🇦": "ar-SA-SanaNeural",
    "Madhur (Hindi - Male) 🇮🇳": "hi-IN-MadhurNeural",
    "Swara (Hindi - Female) 🇮🇳": "hi-IN-SwaraNeural",
    "Pradeep (Bengali - Male) 🇮🇳": "bn-IN-PradeepNeural",
    "Nabanita (Bengali - Female) 🇧🇩": "bn-BD-NabanitaNeural",
    "Latif (Pashto - Male) 🇵🇰": "ps-PK-LatifNeural",
    "Gul Noor (Pashto - Female) 🇦🇫": "ps-AF-GulNoorNeural",
    "Sameer (Sindhi - Male) 🇵🇰": "sd-PK-SameerNeural",
    "Salma (Sindhi - Female) 🇵🇰": "sd-PK-SalmaNeural",
    "Jass (Punjabi - Male) 🇮🇳": "pa-IN-JassNeural",
    "Harpreet (Punjabi - Female) 🇮🇳": "pa-IN-HarpreetNeural",
    "Ahmet (Turkish - Male) 🇹🇷": "tr-TR-AhmetNeural",
    "Emel (Turkish - Female) 🇹🇷": "tr-TR-EmelNeural",
    "Dariush (Persian/Farsi - Male) 🇮🇷": "fa-IR-DariushNeural",
    "Dilara (Persian/Farsi - Female) 🇮🇷": "fa-IR-DilaraNeural",
    "Alvaro (Spanish - Male) 🇪🇸": "es-ES-AlvaroNeural",
    "Elvira (Spanish - Female) 🇪🇸": "es-ES-ElviraNeural",
    "Henri (French - Male) 🇫🇷": "fr-FR-HenriNeural",
    "Denise (French - Female) 🇫🇷": "fr-FR-DeniseNeural"
}

async def generate_voice_tracks(text, voice_id, speed, pitch):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    else:
        for file in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    speed_str = f"{'+' if speed >= 0 else ''}{speed}%"
    pitch_str = f"{'+' if pitch >= 0 else ''}{pitch}Hz"
    
    # Global Multilingual Sentence Punctuation Parser Engine
    sentences = [s.strip() for s in re.split(r'(?<=[.!?|۔؟।])\s+', text) if s.strip()]
    if not sentences:
        return None
    
    generated_files = []
    for index, sentence in enumerate(sentences, start=1):
        output_filename = os.path.join(OUTPUT_DIR, f"track_{index:03d}.mp3")
        communicate = edge_tts.Communicate(
            text=sentence, 
            voice=voice_id, 
            rate=speed_str, 
            pitch=pitch_str
        )
        await communicate.save(output_filename)
        generated_files.append(output_filename)
        
    return generated_files

# --- Premium UI Page Configuration ---
st.set_page_config(page_title="VocalForge AI Studio", page_icon="🎙️", layout="wide")

# --- CSS Injection Phase (100% Responsive Blueprint to prevent UI squeezing) ---
css_lines = [
    "<style>",
    ".stApp { background: transparent !important; position: relative; overflow-x: hidden; padding-bottom: 240px !important; }",
    ".stApp::before { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -2; background-size: cover; background-position: center; background-attachment: fixed; animation: backgroundSlider 24s infinite ease-in-out; }",
    ".stApp::after { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -1; background: linear-gradient(rgba(3, 7, 20, 0.88), rgba(11, 18, 40, 0.97)); pointer-events: none; }",
    "@keyframes backgroundSlider {",
    "  0%, 100% { background-image: url('https://images.unsplash.com/photo-1478737270239-2f02b77fc618'); }",
    "  33% { background-image: url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04'); }",
    "  66% { background-image: url('https://images.unsplash.com/photo-1516280440614-37939bbacd6a'); }",
    "}",
    ".block-container { padding-left: 3rem !important; padding-right: 3rem !important; padding-top: 2rem !important; }",
    "div[data-testid='stVerticalBlock'] > div { position: relative; z-index: 10; }",
    "h1, h2, h3, p, label, span { color: #f8fafc !important; font-weight: 500; white-space: normal !important; }",
    ".stTextArea textarea { background-color: rgba(15, 23, 42, 0.88) !important; color: #f8fafc !important; border: 1px solid rgba(56, 189, 248, 0.35) !important; border-radius: 12px !important; font-size: 16px !important; backdrop-filter: blur(12px); padding: 14px; }",
    ".stTextArea textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 14px rgba(56, 189, 248, 0.5) !important; }",
    ".audio-card { background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); backdrop-filter: blur(12px); }",
    ".audio-card-title { color: #38bdf8 !important; font-weight: 600; font-size: 16px; margin-bottom: 4px; }",
    ".audio-card-meta { color: #94a3b8 !important; font-size: 12px; margin-bottom: 8px; }",
    ".studio-title { background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 2.8rem; margin-bottom: 0.2rem; letter-spacing: 1px; }",
    ".studio-subtitle { color: #cbd5e1; font-size: 1.1rem; margin-bottom: 2.5rem; }",
    ".legal-box { background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 24px; margin-top: 10px; backdrop-filter: blur(12px); }",
    ".bottom-nav-container { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(8, 12, 26, 0.98) !important; backdrop-filter: blur(24px); border-top: 1px solid rgba(56, 189, 248, 0.2); padding: 16px 40px; z-index: 999999; text-align: center; box-shadow: 0 -12px 36px rgba(0,0,0,0.8); }",
    ".bottom-nav-copyright { font-size: 11px; color: #64748b; margin-top: 12px; letter-spacing: 0.5px; }",
    "</style>"
]
css_style = "".join(css_lines)
st.markdown(css_style, unsafe_allow_html=True)

# Navigation State Manager
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎙️ Studio"

page = st.session_state.current_page

# ==============================================================================
# UI ROUTER PAGES RENDER
# ==============================================================================
if page == "🎙️ Studio":
    st.markdown('<div class="studio-title">VOCALFORGE AI STUDIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="studio-subtitle">Global Multi-Voice Sentence Splitter & Generator | ملٹی لنگول اسٹوڈیو</div>', unsafe_allow_html=True)

    # 50-50 Standard Secure Split
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("### 📝 Script Input / یہاں اسکرپٹ لکھیں")
        input_text = st.text_area("Input Text", placeholder="Paste your script here in any language...\nیہاں اپنا اسکرپٹ پیسٹ کریں...", height=250, label_visibility="collapsed")
        
        st.markdown("### ⚙️ Voice Settings / آواز کی سیٹنگز")
        
        selected_voice_label = st.selectbox("Choose Actor Voice / آواز کا انتخاب کریں", options=list(VOICES.keys()), index=0)
        selected_voice_id = VOICES[selected_voice_label]
        
        speed_slider = st.slider("Speed Adjustment (%) / آواز کی رفتار", min_value=-50, max_value=50, value=0, step=1)
        pitch_slider = st.slider("Pitch Adjustment (Hz) / آواز کا پچ", min_value=-20, max_value=20, value=0, step=1)
        
        generate_clicked = st.button("🎙️ Compile Audio Assets / آواز بنائیں", type="primary", use_container_width=True)

    with col_right:
        st.markdown("### 📁 Compiled Voice Tracks / آڈیوز")
        
        if generate_clicked:
            if not input_text.strip():
                st.warning("Please enter some text
