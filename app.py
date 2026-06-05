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

# --- 10 Premium Aesthetic Studio & Abstract Tech Backgrounds ---
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

# --- Premium High Contrast UI CSS Engine ---
css_chunks = [
    "<style>",
    "/* App Container and Golden Cinematic Border Wrapper */",
    ".stApp {",
    "  background: transparent !important;",
    "  overflow-x: hidden;",
    "  padding: 20px !important;",
    "  padding-bottom: 240px !important;",
    "}",
    ".stApp::before {",
    "  content: ''; position: fixed;",
    "  top: 10px; left: 10px; right: 10px; bottom: 10px;",
    "  z-index: -2;",
    "  background-size: cover;",
    "  background-position: center;",
    "  background-repeat: no-repeat;",
    "  border: 3px solid rgba(247, 201, 72, 0.8); /* Solid Gold Frame */",
    "  border-radius: 16px;",
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
    "  top: 10px; left: 10px; right: 10px; bottom: 10px; z-index: -1;",
    "  background: linear-gradient(135deg, rgba(3, 7, 22, 0.96), rgba(6, 13, 30, 0.98));",
    "  border-radius: 14px;",
    "}",
    ".block-container {",
    "  padding: 2rem 3rem !important;",
    "}",
    "/* Voice Settings Premium Title Header - Sharp Gold */",
    ".voice-settings-header {",
    "  font-family: 'Georgia', serif;",
    "  color: #f7c948 !important;",
    "  font-weight: 800;",
    "  font-size: 2.5rem;",
    "  margin-bottom: 1.5rem;",
    "}",
    "/* High Visibility Font Overrides across all Streamlit Elements */",
    "div[data-testid='stWidgetLabel'] p, label, span, p, div {{",
    "  color: #ffffff !important;",
    "  font-weight: 700 !important;",
    "  font-size: 15px !important;",
    "  text-shadow: none !important;",
    "}}",
    "/* Glassmorphism Containers for Inputs with Deep Dark Backgrounds for Text Legibility */",
    "div[data-testid='stSelectbox'], div[data-testid='stSlider'] {",
    "  background: rgba(10, 16, 32, 0.95) !important;",
    "  border: 1.5px solid rgba(255, 255, 255, 0.3) !important;",
    "  border-radius: 10px !important;",
    "  padding: 12px 20px !important;",
    "  margin-bottom: 15px !important;",
    "}",
    "/* Target active selection item text specifically */",
    "div[data-baseweb='select'] div {",
    "  color: #ffffff !important;",
    "  font-weight: 700 !important;",
    "}",
    "/* Custom Style for Text Area */",
    ".stTextArea textarea {",
    "  background-color: rgba(5, 8, 18, 0.95) !important;",
    "  color: #ffffff !important;",
    "  font-weight: 600 !important;",
    "  border: 1.5px solid rgba(247, 201, 72, 0.5) !important;",
    "  border-radius: 12px !important;",
    "}",
    "/* Metallic Center Compilation Button */",
    ".compile-container {",
    "  text-align: center;",
    "  margin: 2rem auto;",
    "  max-width: 500px;",
    "}",
    ".compile-container button {",
    "  background: linear-gradient(180deg, #ffffff 0%, #dddddd 40%, #aaaaaa 100%) !important;",
    "  border: 2px solid #38bdf8 !important;",
    "  border-radius: 12px !important;",
    "  color: #000000 !important; /* Deep black for button text readability */",
    "  font-weight: 900 !important;",
    "  font-size: 16px !important;",
    "  letter-spacing: 1px !important;",
    "  padding: 18px 30px !important;",
    "  height: auto !important;",
    "  width: 100% !important;",
    "  box-shadow: 0 0 25px rgba(56, 189, 248, 0.7) !important;",
    "  text-transform: uppercase;",
    "  transition: all 0.3s ease !important;",
    "}",
    ".compile-container button:hover {",
    "  transform: scale(1.02) !important;",
    "  box-shadow: 0 0 35px rgba(56, 189, 248, 1) !important;",
    "}",
    "/* Bottom Fixed Glass Bar */",
    ".bottom-nav-container {",
    "  position: fixed; bottom: 20px; left: 30px; right: 30px;",
    "  background: rgba(3, 5, 12, 0.98) !important;",
    "  border-top: 2px solid rgba(247, 201, 72, 0.5);",
    "  padding: 20px; z-index: 999999; text-align: center;",
    "  border-radius: 14px;",
    "}",
    "/* Capsule Page Action Buttons */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] button {",
    "  border-radius: 10px !important;",
    "  height: 56px !important;",
    "  width: 100% !important;",
    "  font-size: 15px !important;",
    "  font-weight: 800 !important;",
    "  color: #ffffff !important; ",
    "  border: 1.5px solid rgba(255,255,255,0.4) !important;",
    "  box-shadow: 0 4px 12px rgba(0,0,0,0.6) !important;",
    "  transition: all 0.2s ease !important;",
    "}",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] button:hover {",
    "  transform: translateY(-3px) !important;",
    "}",
    "/* Specific Capsules Gradient Custom Color Nodes mapped to Screenshot */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(1) button { background: linear-gradient(90deg, #1e3a8a, #3b82f6) !important; } /* Studio - Blue */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(2) button { background: linear-gradient(90deg, #064e3b, #10b981) !important; } /* Privacy - Green */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(3) button { background: linear-gradient(90deg, #78350f, #d97706) !important; } /* Terms - Gold/Bronze */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(4) button { background: linear-gradient(90deg, #7f1d1d, #ef4444) !important; } /* Contact - Crimson Red */",
    ".bottom-nav-container div[data-testid='stHorizontalBlock'] div:nth-child(5) button { background: transparent !important; border: 2px dashed #facc15 !important; color: #facc15 !important; } /* Disclaimer - Outlined Glowing Yellow */",
    "</style>"
]
st.markdown("".join(css_chunks), unsafe_allow_html=True)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Studio"

page = st.session_state.current_page

# --- Router Dashboard Layout ---
if page == "Studio":
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown('<h2 class="voice-settings-header">Voice Settings</h2>', unsafe_allow_html=True)
        
        sel_voice = st.selectbox(
            "Select Voice", 
            options=list(VOICES.keys()), 
            index=0
        )
        voice_id = VOICES[sel_voice]
        
        speed = st.slider("Speed", -50, 50, 0, 1)
        pitch = st.slider("Pitch", -20, 20, 0, 1)
        
        st.markdown('<div class="compile-container">', unsafe_allow_html=True)
        generate_clicked = st.button("🎙 * COMPILE & SYNTHESIZE AUDIO *")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<h2 class="voice-settings-header" style="color:#38bdf8;">Script Board</h2>', unsafe_allow_html=True)
        input_text = st.text_area(
            "Input Text Dashboard", 
            placeholder="Enter your sequence narrative workflow scripts here...", 
            height=200, 
            label_visibility="collapsed"
        )
        
        if generate_clicked:
            if not input_text.strip():
                st.warning("Script empty! Please write some lines first.")
            else:
                with st.spinner("Processing Synthesis..."):
                    files = asyncio.run(generate_voice_tracks(input_text, voice_id, speed, pitch))
                    if files:
                        zip_buf = io.BytesIO()
                        with zipfile.ZipFile(zip_buf, "w") as zf:
                            for f_path in files:
                                zf.write(f_path, os.path.basename(f_path))
                        zip_buf.seek(0)
                        
                        st.download_button(
                            label="📦 Download Packaged Tracks (ZIP)",
                            data=zip_buf,
                            file_name="vocalforge_package.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                        
                        for idx, f_path in enumerate(files, start=1):
                            st.audio(f_path)

else:
    st.markdown(f'<h1 class="voice-settings-header">{page} Modules</h1>', unsafe_allow_html=True)
    st.write(f"System loaded sub-environment sequence content for profile partition: {page}")

# --- Bottom Horizontal Navigation Layout ---
st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)
nav_cols = st.columns(5)
p_list = ["Studio", "Privacy", "Terms", "Contact", "Disclaimer"]
icons = ["🎙 ", "🛡 ", "📄 ", "📞 ", "⚠ "]

for i, p_name in enumerate(p_list):
    with nav_cols[i]:
        if st.button(f"{icons[i]}{p_name}", key=f"btn_nav_{i}"):
            st.session_state.current_page = p_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
