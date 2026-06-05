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

# --- 10 Premium Aesthetic Studio Wallpaper Assets ---
img1 = "https://images.unsplash.com/photo-1516280440614-37939bbacd6a"
img2 = "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04"
img3 = "https://images.unsplash.com/photo-1478737270239-2f02b77fc618"
img4 = "https://images.unsplash.com/photo-1520523839897-bd0b52f945a0"
img5 = "https://images.unsplash.com/photo-1484755560693-a4074577af3a"
img6 = "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4"
img7 = "https://images.unsplash.com/photo-1514525253161-7a46d19cd819"
img8 = "https://images.unsplash.com/photo-1459749411175-04bf5292ceea"
img9 = "https://images.unsplash.com/photo-1465847899084-d164df4dedc6"
img10 = "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad"

# --- Infinite CSS Engine with Strict Bottom Nav Circle Targets ---
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
    "  background-attachment: fixed;",
    "  animation: bgInfiniteSlider 60s infinite ease-in-out;",
    "}",
    "@keyframes bgInfiniteSlider {",
    f"  0%, 100% {{ background-image: url('{img1}'); }}",
    f"  10% {{ background-image: url('{img2}'); }}",
    f"  20% {{ background-image: url('{img3}'); }}",
    f"  30% {{ background-image: url('{img4}'); }}",
    f"  40% {{ background-image: url('{img5}'); }}",
    f"  50% {{ background-image: url('{img6}'); }}",
    f"  60% {{ background-image: url('{img7}'); }}",
    f"  70% {{ background-image: url('{img8}'); }}",
    f"  80% {{ background-image: url('{img9}'); }}",
    f"  90% {{ background-image: url('{img10}'); }}",
    "}",
    ".stApp::after {",
    "  content: ''; position: fixed;",
    "  top: 0; left: 0; right: 0; bottom: 0; z-index: -1;",
    "  background: linear-gradient(",
    "    rgba(3, 7, 20, 0.88), rgba(11, 18, 40, 0.95)",
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
    "  padding: 25px 40px; z-index: 999999; text-align: center;",
    "}",
    "/* Isolate Circle Styles specifically to the Bottom Container Columns */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] button {",
    "  border-radius: 50% !important;",
    "  width: 95px !important;",
    "  height: 95px !important;",
    "  padding: 0px !important;",
    "  font-size: 13px !important;",
    "  font-weight: 800 !important;",
    "  color: #000000 !important;",
    "  border: 2px solid #ffffff !important;",
    "  display: inline-flex !important;",
    "  align-items: center !important;",
    "  justify-content: center !important;",
    "  text-align: center !important;",
    "  box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;",
    "  transition: transform 0.2s, box-shadow 0.2s !important;",
    "}",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] button:hover {",
    "  transform: scale(1.1) !important;",
    "  box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4) !important;",
    "}",
    "/* Unique Colors injected per column node */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(1) button { background: #38bdf8 !important; }",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(2) button { background: #34d399 !important; }",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(3) button { background: #fbbf24 !important; }",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(4) button { background: #fb923c !important; }",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(5) button { background: #f472b6 !important; }",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(6) button { background: #a78bfa !important; }",
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
        if st.button(
            p_name, 
            key=f"nav_{i}", 
            use_container_width=True
        ):
            st.session_state.current_page = p_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
