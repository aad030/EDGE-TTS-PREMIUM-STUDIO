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

# --- CSS Injection: Seamless UI with Cross-Fading Voice Studio Slider ---
st.markdown("""
    <style>
    /* Main App Layer Core Setup */
    .stApp {
        background: none !important;
        position: relative;
        overflow: hidden;
        padding-bottom: 160px !important;
    }
    
    /* Background Slider Layer (Stays fixed behind content blocks) */
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

    /* Dark Cyberpunk Gradient Matrix for Text Visibility Protection */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -1;
        background: linear-gradient(rgba(4, 8, 24, 0.78), rgba(12, 20, 42, 0.88));
        pointer-events: none;
    }

    @keyframes backgroundSlider {
        0%, 100% {
            background-image: url("https://images.unsplash.com/photo-1478737270239-2f02b77fc618?q=80&w=2070&auto=format&fit=crop"); /* Studio mic */
        }
        33% {
            background-image: url("https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=2070&auto=format&fit=crop"); /* Equalizer board */
        }
        66% {
            background-image: url("https://images.unsplash.com/photo-1516280440614-37939bbacd6a?q=80&w=2070&auto=format&fit=crop"); /* Audio Frequency */
        }
    }

    /* Streamlit Structural Block Overrides for Proper Layout Rendering */
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
    }
    
    /* Input Form Containers & Custom Cards (Glassmorphic Blueprint) */
    .stTextArea textarea {
        background-color: rgba(11, 19, 41, 0.75) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        backdrop-filter: blur(8px);
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.4) !important;
    }
    
    /* Output Asset Track Elements */
    .audio-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.65), rgba(15, 23, 42, 0.75));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
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
    
    /* Professional Premium Typography Blocks */
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
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-top: 10px;
        backdrop-filter: blur(12px);
    }
    
    /* Fixed Glassmorphic Navigation Component Grid */
    .bottom-nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(8, 12, 26, 0.9) !important;
        backdrop-filter: blur(24px);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 14px 40px;
        z-index: 99999;
        text-align: center;
        box-shadow: 0 -12px 36px rgba(0,0,0,0.65);
    }
    .bottom-nav-copyright {
        font-size: 11px;
        color: #64748b;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Maintain State Navigation Management 
if "current_page" not in st.session
