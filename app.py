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

# --- CSS Injection: Clean Layout with Fixed Voice Studio Wallpaper Slider ---
st.markdown("""
    <style>
    /* Main App Container Core Customization */
    .stApp {
        background: none !important;
        position: relative;
        overflow-x: hidden;
        padding-bottom: 160px !important;
    }
    
    /* Smooth CSS Keyframes for Voice Studio Wallpaper Slider */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -2;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        animation: backgroundSlider 20s infinite ease-in-out;
    }

    /* Dark Overlay Filter Matrix to maintain high text contrast */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -1;
        background: linear-gradient(rgba(1, 4, 18, 0.85), rgba(10, 17, 36, 0.92));
        pointer-events: none;
    }

    @keyframes backgroundSlider {
        0%, 100% {
            background-image: url("https://images.unsplash.com/photo-1478737270239-2f02b77fc618?q=80&w=2070&auto=format&fit=crop");
        }
        33% {
            background-image: url("https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=2070&auto=format&fit=crop");
        }
        66% {
            background-image: url("https://images.unsplash.com/photo-1516280440614-37939bbacd6a?q=80&w=2070&auto=format&fit=crop");
        }
    }

    /* Form Container Setup (Glassmorphism Effect) */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(16px);
    }
    
    /* Input Area Box Control */
    textarea {
        background-color: rgba(11, 19, 41, 0.75) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        backdrop-filter: blur(8px);
    }
    textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }
    
    /* Output Asset Cards */
    .audio-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.7));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(10px);
    }
    .audio-card-title {
        color: #38bdf8;
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .audio-card-meta {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 8px;
    }
    
    /* Typography Overrides */
    .studio-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        text-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
    }
    .studio-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .legal-box {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-top: 10px;
        backdrop-filter: blur(12px);
    }
    
    /* Fixed Glassmorphic Bottom Navigation Controls */
    .bottom-nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(10, 15, 30, 0.88) !important;
        backdrop-filter: blur(24px);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding: 14px 40px;
        z-index: 99999;
        text-align: center;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.6);
    }
    .bottom-nav-copyright {
        font-size: 11px;
        color: #64748b;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Structure for Seamless Updates
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎙️ Studio"

page = st.session_state.current_page

# ==============================================================================
# APP ROUTING INTERFACE
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
                st.warning("Please enter some text first! / پہلے tekst لکھیں!")
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
                            st.markdown(f"""
                                <div class="audio-card">
                                    <div class="audio-card-title">🎵 Track {index:03d}</div>
                                    <div class="audio-card-meta">Voice Model: {selected_voice_label.split(' ')[0]} | Format: MP3 Stereo</div>
                                </div>
                            """, unsafe_allow_html=True)
                            st.audio(file_path)
                    else:
                        st.error("No valid sentence markers found / کوئی جملہ نہیں ملا۔")
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
    st.write("By accessing this website, we assume you accept these terms and conditions down to their deployment metrics.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "ℹ️ About Us":
    st.markdown('<div class="studio-title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("VocalForge AI Studio is a premium utility developed for high-retention automation channels and audio synchronization nodes.")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📧 Contact Us":
    st.markdown('<div class="studio-title">Contact Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("For architectural and code inquiries, drop a line at: `support@vocalforge-studio.example.com`")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚠️ Disclaimer":
    st.markdown('<div class="studio-title">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("This application runs downstream integrations independently and holds no direct endorsement flags with external platforms.")
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# RENDER FIXED BOTTOM NAVIGATION COMPONENT
# ==============================================================================
st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)

nav_cols = st.columns(6)
pages_list = ["🎙️ Studio", "📄 Privacy Policy", "⚖️ Terms & Conditions", "ℹ️ About Us", "📧 Contact Us", "⚠️ Disclaimer"]

for i, p_name in enumerate(pages_list):
    with nav_cols[i]:
        is_active = (st.session_state.current_page == p_name)
        if st.button(p_name, key=f"nav_btn_{i}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.current_page = p_name
            st.rerun()

st.markdown('<div class="bottom-nav-copyright">© 2026 VocalForge AI Studio | All Rights Reserved.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
