import asyncio
import edge_tts
import streamlit as st
import os
import re
import zipfile
import io

OUTPUT_DIR = "output_voices"

# Premium Voices Mapping (Urdu + English Top Tier)
VOICES = {
    "Asad (Urdu - Male) 🇵🇰": "ur-PK-AsadNeural",
    "Uzma (Urdu - Female) 🇵🇰": "ur-PK-UzmaNeural",
    "Christopher (English - Male) 🇺🇸": "en-US-ChristopherNeural",
    "Ava (English - Female) 🇺🇸": "en-US-AvaNeural"
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
    
    # English (.!?) aur Urdu (۔؟) dono characters par split karega
    sentences = [s.strip() for s in re.split(r'(?<=[.!?|۔؟])\s+', text) if s.strip()]
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
st.set_page_config(page_title="Premium Edge TTS Studio", page_icon="🎙️", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="studio-title">EDGE TTS PREMIUM STUDIO</div>', unsafe_allow_html=True)
st.markdown('<div class="studio-subtitle">Multi-Voice Sentence Splitter & Generator | ملٹی وائس اسٹوڈیو</div>', unsafe_allow_html=True)

# Layout Setup
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown("### 📝 Script Input / یہاں اسکرپٹ لکھیں")
    
    # Input Area
    input_text = st.text_area("Input Text", placeholder="Paste your script here (English or Urdu)... \nیہاں اپنا انگلش یا اردو اسکرپٹ پیسٹ کریں۔", height=240, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Voice Settings / آواز کی سیٹنگز")
    
    # Premium Voice Selector Dropdown
    selected_voice_label = st.selectbox(
        "Choose Actor Voice / آواز کا انتخاب کریں", 
        options=list(VOICES.keys()),
        index=0
    )
    selected_voice_id = VOICES[selected_voice_label]
    
    # Audio Adjustments
    c1, c2 = st.columns(2)
    with c1:
        speed_slider = st.slider("Speed Adjustment (%) / آواز کی رفتار", min_value=-50, max_value=50, value=0, step=1)
    with c2:
        pitch_slider = st.slider("Pitch Adjustment (Hz) / آواز کا پچ", min_value=-20, max_value=20, value=0, step=1)
    
    # Modern Generate Button
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
                    
                    # Creating Zip package
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                        for file_path in files:
                            zip_file.write(file_path, os.path.basename(file_path))
                    zip_buffer.seek(0)
                    
                    # Premium Bulk Download Box
                    st.download_button(
                        label="🚀 Export All Tracks to Timeline (ZIP)",
                        data=zip_buffer,
                        file_name="premium_voice_pack.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                    st.markdown("---")
                    
                    # Visual asset queue with custom cards
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