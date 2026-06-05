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

# --- Custom Premium Dark CSS with Dynamic Wallpaper Background & Fixed Bottom Nav ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(2, 6, 23, 0.75), rgba(15, 23, 42, 0.85)), 
                          url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f8fafc;
        padding-bottom: 120px !important; /* Space for bottom nav */
    }
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(16px);
    }
    textarea {
        background-color: rgba(11, 19, 41, 0.7) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        backdrop-filter: blur(8px);
    }
    textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
    }
    .audio-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.65));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
    .studio-title {
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
        text-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    .studio-subtitle {
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .legal-box {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-top: 10px;
        backdrop-filter: blur(12px);
    }
    
    /* Bottom Navigation Bar Container Styling */
    .bottom-nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 10px 40px;
        z-index: 99999;
        text-align: center;
    }
    .bottom-nav-copyright {
        font-size: 11px;
        color: #64748b;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Page Navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎙️ Studio"

# Get current page to render content
page = st.session_state.current_page

# ==============================================================================
# PAGE RENDER LOGIC
# ==============================================================================
if page == "🎙️ Studio":
    st.markdown('<div class="studio-title">VOCALFORGE AI STUDIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="studio-subtitle">Global Multi-Voice Sentence Splitter & Generator | ملٹی لنگول اسٹوڈیو</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown("### 📝 Script Input / یہاں اسکرپٹ لکھیں")
        input_text = st.text_area("Input Text", placeholder="Paste your script here in any language... \nیہاں apna script paste karein...", height=240, label_visibility="collapsed")
        
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
                            filename = os.path.basename(file_path)
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
    st.write("""
    Welcome to the **VocalForge AI Studio**. This web utility leverages advanced cognitive neural speech architectures to transform multilingual textual content into modular audio elements. 
    Whether you are building cash-cow automation workflows or highly engaging cinematic documentaries across multiple global languages, our system eliminates manual splitting pipelines.
    """)

elif page == "📄 Privacy Policy":
    st.markdown('<div class="studio-title">Privacy Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    At VocalForge AI Studio, accessible from this web application, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by our platform and how we use it.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚖️ Terms & Conditions":
    st.markdown('<div class="studio-title">Terms & Conditions</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    Welcome to VocalForge AI Studio! By accessing this website, we assume you accept these terms and conditions. Do not continue to use VocalForge AI Studio if you do not agree to take all of the terms and conditions stated on this page.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "ℹ️ About Us":
    st.markdown('<div class="studio-title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("""
    ### Welcome to VocalForge AI Studio
    VocalForge AI Studio is a cutting-edge web utility engineered specifically for next-generation content creators, video editors, and cross-platform automation specialists.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📧 Contact Us":
    st.markdown('<div class="studio-title">Contact Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("""
    If you have any questions, feedback, feature requests, or technical inquiries regarding our studio application, feel free to reach out to us.
    ### 📩 Contact Channels
    * **Email Support:** `support@vocalforge-studio.example.com`
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "⚠️ Disclaimer":
    st.markdown('<div class="studio-title">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    All the information and tools on this website are published in good faith and for general information and productivity purposes only.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# INJECTED FIXED BOTTOM NAVIGATION BAR
# ==============================================================================
st.markdown('<div class="bottom-nav-container">', unsafe_allow_html=True)

# Streamlit ke elements column wise alignment mein horizontal render honge
nav_cols = st.columns(6)
pages_list = ["🎙️ Studio", "📄 Privacy Policy", "⚖️ Terms & Conditions", "ℹ️ About Us", "📧 Contact Us", "⚠️ Disclaimer"]

for i, p_name in enumerate(pages_list):
    with nav_cols[i]:
        # Active page ka button alag look dega
        is_active = (st.session_state.current_page == p_name)
        if st.button(p_name, key=f"nav_btn_{i}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state.current_page = p_name
            st.rerun()

st.markdown('<div class="bottom-nav-copyright">© 2026 VocalForge AI Studio | All Rights Reserved.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
