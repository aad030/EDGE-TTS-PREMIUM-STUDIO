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

# --- Custom Premium Dark CSS ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #0f172a, #020617);
        color: #f8fafc;
    }
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px);
    }
    textarea {
        background-color: #0b1329 !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        font-size: 16px !important;
    }
    textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.2) !important;
    }
    .audio-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
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
        color: #64748b;
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
    }
    .studio-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .legal-box {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation Menu (AdSense Requirement) ---
st.sidebar.markdown("## 🧭 Navigation")
page = st.sidebar.radio(
    "Go to:",
    ["🎙️ Studio", "📄 Privacy Policy", "⚖️ Terms & Conditions", "ℹ️ About Us", "📧 Contact Us", "⚠️ Disclaimer"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("© 2026 VocalForge AI Studio | All Rights Reserved.")

# ==============================================================================
# PAGE 1: MAIN STUDIO
# ==============================================================================
if page == "🎙️ Studio":
    st.markdown('<div class="studio-title">VOCALFORGE AI STUDIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="studio-subtitle">Global Multi-Voice Sentence Splitter & Generator | ملٹی لنگول اسٹوڈیو</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        st.markdown("### 📝 Script Input / یہاں اسکرپٹ لکھیں")
        input_text = st.text_area("Input Text", placeholder="Paste your script here in any language... \nیہاں اپنا اسکرپٹ پیسٹ کریں۔", height=240, label_visibility="collapsed")
        
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
    
    #### How It Works:
    1. **Text Segmentation:** The backend parsing engine processes inputs and tokenizes textual information based on language-specific sentence terminators like periods (`.`), khatma (`۔`), poorna viram (`।`), or global punctuation marks.
    2. **Neural Synthesizing:** Selected vocal models process individual data tracks independently using asynchronous execution routines to maintain high performance.
    3. **Timeline Deployment:** Audio outputs are delivered sequentially (`track_001.mp3`, `track_002.mp3`), making it instantly compatible with editing software like Adobe Premiere Pro, CapCut, or DaVinci Resolve.
    """)

# ==============================================================================
# PAGE 2: PRIVACY POLICY
# ==============================================================================
elif page == "📄 Privacy Policy":
    st.markdown('<div class="studio-title">Privacy Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    At VocalForge AI Studio, accessible from this web application, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by our platform and how we use it.

    ### 1. Log Files
    VocalForge AI Studio follows a standard procedure of using log files. These files log visitors when they visit web applications. The information collected by log files includes internet protocol (IP) addresses, browser type, Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the number of clicks. These are not linked to any information that is personally identifiable.

    ### 2. Cookies and Web Beacons
    Like any other website, our studio uses 'cookies'. These cookies are used to store information including visitors' preferences, and the pages on the website that the visitor accessed or visited. The information is used to optimize the users' experience by customizing our web page content based on visitors' browser type and/or other information.

    ### 3. Google DoubleClick DART Cookie
    Google is one of the third-party vendors on our site. It also uses cookies, known as DART cookies, to serve ads to our site visitors based upon their visit to our platform and other sites on the internet. However, visitors may choose to decline the use of DART cookies by visiting the Google ad and content network Privacy Policy.

    ### 4. Third-Party Privacy Policies
    Our platform's Privacy Policy does not apply to other advertisers or websites. Thus, we are advising you to consult the respective Privacy Policies of these third-party ad servers for more detailed information. It may include their practices and instructions about how to opt-out of certain options.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PAGE 3: TERMS & CONDITIONS
# ==============================================================================
elif page == "⚖️ Terms & Conditions":
    st.markdown('<div class="studio-title">Terms & Conditions</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    Welcome to VocalForge AI Studio! By accessing this website, we assume you accept these terms and conditions. Do not continue to use VocalForge AI Studio if you do not agree to take all of the terms and conditions stated on this page.

    ### 1. License & Intellectual Property
    Unless otherwise stated, VocalForge AI Studio and/or its licensors own the intellectual property rights for all code and material on this application. All intellectual property rights are reserved. You may access this from VocalForge AI Studio for your own personal use subjected to restrictions set in these terms and conditions.

    ### 2. User Restrictions
    You are specifically restricted from all of the following:
    * Publishing our application code anywhere without appropriate attribution.
    * Selling, sublicensing, and/or otherwise commercializing any website material.
    * Using this application in any way that is or may be damaging to this website.
    * Using this application contrary to applicable laws and regulations.

    ### 3. Voice Assets Usage
    The voice generation functionality utilizes experimental downstream API libraries. Users are solely responsible for ensuring that the voice assets generated conform to the content policy parameters of their chosen publication platforms (e.g., YouTube, TikTok).
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PAGE 4: ABOUT US
# ==============================================================================
elif page == "ℹ️ About Us":
    st.markdown('<div class="studio-title">About Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("""
    ### Welcome to VocalForge AI Studio

    VocalForge AI Studio is a cutting-edge web utility engineered specifically for next-generation content creators, video editors, and cross-platform automation specialists. Our primary mission is to simplify the content synthesis workflow by bridging the gap between sophisticated neural audio models and modern non-linear editing (NLE) suites.

    #### Why Choose Us?
    Traditional Text-to-Speech solutions generate massive, single-track audio blocks that require hours of meticulous splicing on editing timelines. VocalForge AI Studio dynamically parses textual scripts into logical linguistic elements, synthesizing independent, high-fidelity sound tracks in structural sequence across an extensive catalog of global languages including Urdu, English, Hindi, Arabic, Bengali, Pashto, Sindhi, Punjabi, Turkish, Persian, Spanish, and French.

    #### Core Values
    * **Efficiency:** Minimizing time spent on asset slicing.
    * **Accessibility:** Providing clean open-source frameworks for developers globally.
    * **Innovation:** Utilizing modern asynchronous workflows for swift production pipelines.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PAGE 5: CONTACT US
# ==============================================================================
elif page == "📧 Contact Us":
    st.markdown('<div class="studio-title">Contact Us</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("""
    If you have any questions, feedback, feature requests, or technical inquiries regarding our studio application, feel free to reach out to us. We aim to respond within 24 to 48 hours.

    ### 📩 Contact Channels
    * **Email Support:** `support@vocalforge-studio.example.com`
    * **Developer Repository:** Feel free to open an issue on our official GitHub repository for bugs or code improvements.
    * **Social Presence:** Connect with our official development profile on Twitter (X) for tech updates.

    *Note: Please avoid sharing any sensitive credential configurations or personal access tokens when initiating support requests.*
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PAGE 6: DISCLAIMER
# ==============================================================================
elif page == "⚠️ Disclaimer":
    st.markdown('<div class="studio-title">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">', unsafe_allow_html=True)
    st.write("**Last Updated: June 2026**")
    st.write("""
    ### 1. General Information Only
    All the information and tools on this website are published in good faith and for general information and productivity purposes only. VocalForge AI Studio does not make any warranties about the completeness, reliability, and accuracy of this utility. Any action you take upon the information you find on this website is strictly at your own risk.

    ### 2. Third-Party Affiliation
    This application is an independent development project. It is **not** officially affiliated with, endorsed by, sponsored by, or in any way connected to Microsoft Corporation or any of its subsidiaries. The voice assets and underlying synthesizer models are powered by the available `edge-tts` python execution layer.

    ### 3. Financial and Liability Limitation
    In no event will VocalForge AI Studio be liable for any loss or damage including without limitation, indirect or consequential loss or damage, arising from loss of data or production timeline delays in connection with the use of this free tool.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
