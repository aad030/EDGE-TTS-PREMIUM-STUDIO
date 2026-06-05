2. Hamare functional components mein `asyncio.run()` runtime generator pass karna hoga taake user ka input text directly Microsoft Server nodes par process ho kar `.mp3` format return kare.

Niche complete functional production code module diya gaya hai jise aap directly copy-paste kar sakte hain:

```python
import streamlit as st
import asyncio
import edge_tts
import os

# --- Session State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'Studio'

# --- Premium Languages & Accents Unified Data Matrix ---
VOICE_DATA = {
    "Urdu 🇵🇰": {"color": "#fbbf24", "voice": "ur-PK-AsadNeural"},
    "English 🇺🇸": {"color": "#38bdf8", "voice": "en-US-ChristopherNeural"}, # Premium Christopher voice route
    "Arabic 🇸🇦": {"color": "#34d399", "voice": "ar-SA-HamedNeural"},
    "Hindi 🇮🇳": {"color": "#f472b6", "voice": "hi-IN-MadhurNeural"},
    "Spanish 🇪🇸": {"color": "#fb923c", "voice": "es-ES-AlvaroNeural"},
    "Russian 🇷🇺": {"color": "#a78bfa", "voice": "ru-RU-DmitryNeural"},
    "Japanese 🇯🇵": {"color": "#f87171", "voice": "ja-JP-KeitaNeural"},
    "Chinese 🇨🇳": {"color": "#60a5fa", "voice": "zh-CN-YunxiNeural"}
}

# --- Asynchronous Neural Generation Core Engine ---
async def generate_neural_voice(text_payload, voice_model, speed_offset, pitch_offset) -> str:
    output_filename = "synthesized_studio_output.mp3"
    
    # Mathematical scaling formats matching structural edge syntax rules
    speed_parameter = f"{'+' if speed_offset >= 0 else ''}{speed_offset}%"
    pitch_parameter = f"{'+' if pitch_offset >= 0 else ''}{pitch_offset}Hz"
    
    # Instantiating edge transaction
    communication_node = edge_tts.Communicate(
        text=text_payload, 
        voice=voice_model, 
        rate=speed_parameter, 
        pitch=pitch_parameter
    )
    await communication_node.save(output_filename)
    return output_filename

# --- Page Configuration ---
st.set_page_config(page_title="VocalNexus AI", layout="wide")

# --- Premium Design Engine (Strict Glitch Target Blocks) ---
css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Font Overrides */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3, h4 { 
        font-family: 'Montserrat', sans-serif !important; 
        font-weight: 700 !important; 
    }
    
    /* Dark Cinematic Background */
    .stApp { background-color: #030712 !important; }
    
    /* STRICT GLITCH FIX: Target and vanish the 'double_arrow_right' raw string element */
    button[data-testid="collapsedControl"], 
    button[data-testid="collapsedControl"] *, 
    [data-testid="collapsedControl"] span,
    div[class*="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        font-size: 0px !important;
        color: transparent !important;
        width: 0px !important;
        height: 0px !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { 
        background-color: #0a0f1d !important; 
        border-right: 1px solid #1e293b !important; 
    }
    
    /* Dropdown UI Refinement */
    div[data-baseweb="select"] {
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        background: #0f172a !important;
    }
    
    /* Metallic Glass Capsule Sliders */
    div[data-testid="stSlider"] {
        background: linear-gradient(145deg, #111827, #1f2937) !important;
        padding: 15px 25px !important;
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        margin-bottom: 15px !important;
    }
    
    /* Professional Action Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #d4af37, #aa882c) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: transform 0.2s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Universal Text Visibility */
    h1, h2, h3, h4, label, p, li { color: #ffffff !important; }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; margin-bottom: 0;'>🎙️ VocalNexus AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b !important; font-size: 14px;'>Next-Gen Neural Audio</p>", unsafe_allow_html=True)
    st.divider()
    
    pages = ["Studio", "About Us", "Privacy", "Terms", "Contact", "Disclaimer"]
    for page in pages:
        if st.button(page, use_container_width=True):
            st.session_state.page = page
            st.rerun()

# --- Page Router & Content Implementation ---
if st.session_state.page == 'Studio':
    st.markdown("## Studio Dashboard")
    st.markdown("Configure your neural voice parameters and workflow sequence below.")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### Voice Settings")
        selected_lang = st.selectbox("Select Language & Accent", list(VOICE_DATA.keys()))
        
        # Access parameters securely via data mapping nested dictionary
        accent_color = VOICE_DATA[selected_lang]["color"]
        voice_model_key = VOICE_DATA[selected_lang]["voice"]
        
        st.markdown(f"<span style='background-color: {accent_color}20; color: {accent_color}; border: 1px solid {accent_color}; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;'>Active Model: {selected_lang}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # UI Tuning Nodes
        speed = st.slider("Speed (Tempo %)", -50, 50, 0)
        pitch = st.slider("Pitch (Frequency Hz)", -20, 20, 0)
        
    with col2:
        st.markdown("### Script Board")
        script_payload = st.text_area("Workflow Sequence", height=220, placeholder="Enter your sequence narrative text here...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎙️ Compile & Synthesize"):
            if not script_payload.strip():
                st.error("Error: Script Board parameter context cannot be empty node vector value.")
            else:
                with st.spinner("Executing dynamic structural runtime conversion pipelines..."):
                    try:
                        # Direct loop threading interface execution mapping
                        generated_audio_path = asyncio.run(
                            generate_neural_voice(script_payload, voice_model_key, speed, pitch)
                        )
                        
                        if os.path.exists(generated_audio_path):
                            st.success("Neural Audio Compiled Successfully!")
                            # Injecting native custom streamlined HTML player block directly inside view column
                            st.audio(generated_audio_path, format="audio/mp3")
                    except Exception as failure_exception:
                        st.error(f"Execution Error Encountered: {str(failure_exception)}")

elif st.session_state.page == 'About Us':
    st.markdown("## Corporate Overview & Vision")
    st.markdown("---")
    st.markdown("""
    ### 1. Our Identity
    VocalNexus AI stands at the absolute vanguard of advanced speech synthesis technologies. We develop and curate enterprise-grade neural audio processing algorithms designed for modern content creators, digital production networks, and global automation ecosystems.
    """)

elif st.session_state.page == 'Privacy':
    st.markdown("## Data Privacy & Encryption Infrastructure")
    st.markdown("---")
    st.markdown("""
    ### 1. Scope of Data Governance
    At VocalNexus AI, safeguarding user information is fundamentally wired into our design principles.
    """)

elif st.session_state.page == 'Terms':
    st.markdown("## Global Terms of Service & Licensing Framework")
    st.markdown("---")
    st.markdown("""
    ### 1. Mutual Contractual Agreement
    By accessing or communicating with the underlying software instances of VocalNexus AI, you unconditionally consent to comply with the comprehensive legal parameters documented herein.
    """)

elif st.session_state.page == 'Contact':
    st.markdown("## Enterprise Operations & Engineering Support")
    st.markdown("---")
    st.markdown("""
    ### 1. Global Technical Escalations
    For complex infrastructure integrations, automated script-writing node deployments, API access initialization, or platform failures, please reach our systems engineering network directly.
    """)

elif st.session_state.page == 'Disclaimer':
    st.markdown("## Comprehensive Legal Risk Disclaimer")
    st.markdown("---")
    st.markdown("""
    ### 1. General Nature of Synthetic Utilities
    VocalNexus AI functions strictly as an AI-augmented conversion tool.
    """)
