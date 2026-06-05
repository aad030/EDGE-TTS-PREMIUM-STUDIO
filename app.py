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

# --- CSS Injection: Fixed Layout with Dynamic Voice Studio Slider ---
st.markdown("""
    <style>
    /* Main App Container Core Customization */
    .stApp {
        background: none !important;
        position: relative;
        overflow-x: hidden;
        padding-bottom: 160px !important;
        color: #f8fafc !important;
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
        background: linear-gradient(rgba(1, 4, 18, 0.82), rgba(10, 17, 36, 0.9));
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
        backdrop-filter
