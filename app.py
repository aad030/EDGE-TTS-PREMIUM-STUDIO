import asyncio
import edge_tts
import streamlit as st
import os
import re
import zipfile
import io

OUTPUT_DIR = "output_voices"

VOICES = {
    "Asad (Urdu) 🇵🇰": "ur-PK-AsadNeural",
    "Uzma (Urdu) 🇵🇰": "ur-PK-UzmaNeural",
    "Christopher (Eng) 🇺🇸": "en-US-ChristopherNeural",
    "Ava (English) 🇺🇸": "en-US-AvaNeural",
    "Hamed (Arabic) 🇸🇦": "ar-SA-HamedNeural",
    "Sana (Arabic) 🇸🇦": "ar-SA-SanaNeural",
    "Madhur (Hindi) 🇮🇳": "hi-IN-MadhurNeural",
    "Swara (Hindi) 🇮🇳": "hi-IN-SwaraNeural"
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
    
    sentences = [
        s.strip() for s in re.split(r'(?<=[.!?|۔؟।])\s+', text) if s.strip()
    ]
    if not sentences:
        return None
    
    generated_files = []
    for index, sentence in enumerate(sentences, start=1):
        out_name = os.path.join(OUTPUT_DIR, f"track_{index:03d}.mp3")
        communicate = edge_tts.Communicate(
            text=sentence, 
            voice=voice_id, 
            rate=speed_str, 
            pitch=pitch_str
        )
        await communicate.save(out_name)
        generated_files.append(out_name)
        
    return generated_files

# --- Page Setup ---
st.set_page_config(
    page_title="VocalForge Studio", 
    page_icon="🎙️", 
    layout="wide"
)

# --- CSS Array (Animations Removed - Clean Static BG) ---
css_chunks = [
    "<style>",
    ".stApp {",
    "  background: transparent !important;",
    "  overflow-x: hidden;",
    "  padding-bottom: 280px !important;",
    "}",
    ".stApp::before {",
    "  content: ''; position: fixed;",
    "  top: 0; left: 0; right: 0; bottom: 0; z-index: -2;",
    "  background-size: cover;",
    "  background-position: center;",
    "  background-repeat: no-repeat;",
    "  background-image: url(",
    "    'https://images.unsplash.com/photo-1516280440614-37939bbacd6a'",
    "  );",
    "}",
    ".stApp::after {",
    "  content: ''; position: fixed;",
    "  top: 0; left: 0; right: 0; bottom: 0; z-index: -1;",
    "  background: linear-gradient(",
    "    rgba(3, 7, 20, 0.9), rgba(11, 18, 40, 0.98)",
    "  );",
    "}",
    ".block-container {",
    "  padding: 2.5rem 3.5rem !important;",
    "}",
    "h1, h2, h3, p, label, span {",
    "  color: #f8fafc !important;",
    "  white-space: normal !important;",
    "}",
    ".stTextArea textarea {",
    "  background-color: rgba(15, 23, 42, 0.95) !important;",
    "  color: #f8fafc !important;",
    "  border: 1px solid rgba(56, 189, 248, 0.4) !important;",
    "  border-radius: 12px !important;",
    "}",
    ".audio-card {",
    "  background: rgba(30, 41, 59, 0.9);",
    "  border: 1px solid rgba(56, 189, 248, 0.3);",
    "  border-radius: 12px; padding: 16px; margin-bottom: 14px;",
    "}",
    ".audio-card-title {",
    "  color: #38bdf8 !important; font-weight: 600;",
    "}",
    ".studio-title {",
    "  font-weight: 800; font-size: 2.5rem;",
    "  color: #38bdf8 !important;",
    "}",
    ".bottom-nav-container {",
    "  position: fixed; bottom: 0; left: 0; right: 0;",
    "  background: #080c1a !important;",
    "  border-top: 1px solid rgba(56, 189, 248, 0.3);",
    "  padding: 15px 40px; z-index: 999999; text-align: center;",
    "}",
    "</style>"
]
st.markdown("".join(css_chunks), unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "🎙️ Studio"

page = st.session_state.current_page

# --- Router ---
if page == "🎙️ Studio":
    st.markdown(
        '<h1 class="studio-title">VOCALFORGE AI STUDIO</h1>', 
        unsafe_allow_html=True
    )
    st.write("Global Multi-Voice Splitter | ملٹی لنگول اسٹوڈیو")

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.subheader("📝 Script Input")
        input_text = st.text_area(
            "Input Text", 
            placeholder="Paste script here...", 
            height=220, 
            label_visibility="collapsed"
        )
        
        st.subheader("⚙️ Voice Settings")
        sel_voice = st.selectbox(
            "Select Voice / آواز", 
            options=list(VOICES.keys()), 
            index=0
        )
        voice_id = VOICES[sel_voice]
        
        speed = st.slider("Speed (%)", -50, 50, 0, 1)
        pitch = st.slider("Pitch (Hz)", -20, 20, 0, 1)
        
        generate_clicked = st.button(
            "🎙️ Compile Audio Assets", 
            type="primary", 
            use_container_width=True
        )

    with col_right:
        st.subheader("📁 Compiled Voice Tracks")
        
        if generate_clicked:
            if not input_text.strip():
                st.warning("Please enter some text first!")
            else:
                with st.spinner("Compiling tracks..."):
                    files = asyncio.run(
                        generate_voice_tracks(
                            input_text, voice_id, speed, pitch
                        )
                    )
                    
                    if files:
                        st.toast("Tracks compiled!")
                        zip_buf = io.BytesIO()
                        with zipfile.ZipFile(zip_buf, "w") as zf:
                            for f_path in files:
                                zf.write(f_path, os.path.basename(f_path))
                        zip_buf.seek(0)
                        
                        st.download_button(
                            label="🚀 Export All Tracks (ZIP)",
                            data=zip_buf,
                            file_name="vocalforge_tracks.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
                        for idx, f_path in enumerate(files, start=1):
                            st.markdown(
                                f'<div class="audio-card">'
                                f'<div class="audio-card-title">'
                                f'🎵 Track {idx:03d}</div></div>', 
                                unsafe_allow_html=True
                            )
                            st.audio(f_path)
                    else:
                        st.error("No valid sentences found.")
        else:
            st.info("System standby. Enter text and compile.")

else:
    st.markdown(
        f'<h1 class="studio-title">{page}</h1>', 
        unsafe_allow_html=True
    )
    st.write("Dynamic local module content loaded successfully.")

# --- Bottom Navigation ---
st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)
nav_cols = st.columns(6)
p_list = [
    "🎙️ Studio", "📄 Privacy", "⚖️ Terms", 
    "ℹ️ About", "📧 Contact", "⚠️ Disclaimer"
]

for i, p_name in enumerate(p_list):
    with nav_cols[i]:
        is_act = (st.session_state.current_page == p_name)
        if st.button(
            p_name, 
            key=f"nav_{i}", 
            use_container_width=True, 
            type="primary" if is_act else "secondary"
        ):
            st.session_state.current_page = p_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
