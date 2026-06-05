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

# --- CSS Injection Phase (Using clean concatenated layout format to bypass string breaks) ---
css_style = """
<style>
.stApp {
    background: transparent !important;
    position: relative;
    overflow-x: hidden;
    padding-bottom: 180px !important;
}
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -2;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    animation: backgroundSlider 24s infinite ease-in-out;
}
.stApp::after {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    background: linear-gradient(rgba(3, 7, 20, 0.85), rgba(11, 18, 40, 0.95));
    pointer-events: none;
}
@keyframes backgroundSlider {
    0%, 100% { background-image: url('https://images.unsplash.com/photo-1478737270239-2f02b77fc618?q=80&w=2070&auto=format&fit=crop'); }
    33% { background-image: url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=2070&auto=format&fit=crop'); }
    66% { background-image: url('https://images.unsplash.com/photo-1516280440614-37939bbacd6a?q=80&w=2070&auto=format&fit=crop'); }
}
div[data-testid="stVerticalBlock"] > div {
    position: relative;
    z-index: 10;
}
h1, h2, h3, p, label, span {
    color: #f8fafc !important;
}
.stTextArea textarea {
    background-color: rgba(11, 19, 41, 0.8) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    backdrop-filter: blur(10px);
}
.stTextArea textarea:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
}
.audio-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
    backdrop-filter: blur(12px);
}
.audio-card-title {
    color: #38bdf8 !important;
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 4px;
}
.audio-card-meta {
    color: #94a3b8 !important;
    font-size: 12px;
    margin-bottom: 8px;
}
.studio-title {
    background: linear-gradient(to right, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.6rem;
    margin-bottom: 0.1rem;
    letter-spacing: 1px;
}
.studio-subtitle {
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 2.2rem;
}
.legal-box {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    margin-top: 10px;
    backdrop-filter: blur(12px);
}
.bottom-nav-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(8, 12, 26, 0.95) !important;
    backdrop-filter: blur(24px);
    border-top: 1px solid rgba(255, 255, 255, 0.12);
    padding: 14px 40px;
    z-index: 999999;
    text-align: center;
    box-shadow: 0 -12px 36px rgba(0,0,0,0.7);
}
.bottom-nav-copyright {
    font-size: 11px;
    color: #64748b;
    margin-top: 10px;
}
</style>
"""
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

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown("### 📝 Script Input / یہاں اسکرپٹ لکھیں")
        input_text = st.text_area("Input Text", placeholder="Paste your script here in any language... \nیہاں اپنا اسکرپٹ پیسٹ کریں...", height=240, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Voice Settings / آواز کی سیٹنگز")
        
        selected_voice_label = st.selectbox("Choose Actor Voice / آواز کا انتخاب کریں", options=list(VOICES.keys()), index=0)
        selected_voice_id = VOICES[selected_voice_label]
        
        c1, c2 = st.columns(2)
        with c1:
            speed_slider = st.slider("Speed Adjustment (%) / آواز کی رفتار", min_value=-50, max_value=50, value=0, step=1)
        with c2:
            pitch_slider = st.slider("Pitch Adjustment (Hz) / آواز کا پچ", min_value=-20, max_value=20, value=0, step=1)
        
        generate_clicked = st.button("🎙️ Compile Audio Assets / آواز بنائیں", type="primary", use_container_width=True)

    with col_right:
        st.markdown("### 📁 Compiled Voice Tracks / آڈیوز")
        
        if generate_clicked:
            if not input_text.strip():
                st.warning("Please enter some text first! / پہلے ٹیکسٹ لکھیں!")
            else:
                with st.spinner("Compiling high-retention tracks... Please wait."):
                    files = asyncio.run(generate_voice_tracks(input_text, selected_voice_id, speed_slider, pitch_slider))
                    
                    if files:
                        st.toast("Tracks compiled successfully!", icon="🔥")
                        
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                            for file_path in files:
                                zip_file.write(file_path, os.path.basename(file_path))
                        zip_buffer.seek(0)
                        
                        st.download_button(
                            label="🚀 Export All Tracks to Timeline (ZIP)",
                            data=zip_buffer,
                            file_name="vocalforge_voice_pack.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
                        st.markdown("---")
                        
                        for index, file_path in enumerate(files, start=1):
                            # Safe formatted injection for track mapping
                            st.markdown(f'<div class="audio-card"><div class="audio-card-title">🎵 Track {index:03d}</div><div class="audio-card-meta">Voice Model: {selected_voice_label.split(" ")[0]} | Format: MP3 Stereo</div></div>', unsafe_allow_html=True)
                            st.audio(file_path)
                    else:
                        st.error("No valid sentence markers found / کوئی جملہ nahi mila.")
        else:
            st.info("System standby. Select voice profile, enter script and click compile.")

    st.markdown("---")
    st.markdown("### 📘 Detailed User Guide & Feature Overview")
    st.write("Welcome to VocalForge AI Studio. This engine tokenizes texts via termination delimiters and passes them into highly descriptive audio layers sequentially.")

elif page == "📄 Privacy Policy":
    st.markdown('<div class="studio-title">Privacy Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("At VocalForge AI Studio, accessible from this web application, one of our main priorities is the privacy of our visitors.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚖️ Terms & Conditions":
    st.markdown('<div class="studio-title">Terms & Conditions</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("By accessing this website, we assume you
