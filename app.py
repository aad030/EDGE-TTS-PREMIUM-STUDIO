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

# --- CSS Injection Phase (Safe Standard Code Concatenation) ---
css_lines = [
    "<style>",
    ".stApp { background: transparent !important; position: relative; overflow-x: hidden; padding-bottom: 260px !important; }",
    ".stApp::before { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -2; background-size: cover; background-position: center; background-attachment: fixed; animation: backgroundSlider 24s infinite ease-in-out; }",
    ".stApp::after { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -1; background: linear-gradient(rgba(3, 7, 20, 0.88), rgba(11, 18, 40, 0.97)); pointer-events: none; }",
    "@keyframes backgroundSlider {",
    "  0%, 100% { background-image: url('https://images.unsplash.com/photo-1478737270239-2f02b77fc618'); }",
    "  33% { background-image: url('https://images.unsplash.com/photo-1598488035139-bdbb2231ce04'); }",
    "  66% { background-image: url('https://images.unsplash.com/photo-1516280440614-37939bbacd6a'); }",
    "}",
    ".block-container { padding-left: 3.5rem !important; padding-right: 3.5rem !important; padding-top: 2.5rem !important; }",
    "div[data-testid='stVerticalBlock'] > div { position: relative; z-index: 10; overflow: visible !important; }",
    "h1, h2, h3, p, label, span { color: #f8fafc !important; font-weight: 500; white-space: normal !important; overflow: visible !important; }",
    ".stTextArea textarea { background-color: rgba(15, 23, 42, 0.92) !important; color: #f8fafc !important; border: 1px solid rgba(56, 189, 248, 0.4) !important; border-radius: 12px !important; font-size: 16px !important; backdrop-filter: blur(12px); padding: 14px; }",
    ".stTextArea textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 14px rgba(56, 189, 248, 0.5) !important; }",
    ".audio-card { background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95)); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 16px; margin-
