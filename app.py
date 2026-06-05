import streamlit as st

# --- Session State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'Studio'

# --- Premium Languages & Accents Data ---
VOICE_DATA = {
    "Urdu 🇵🇰": "#fbbf24",
    "English 🇺🇸": "#38bdf8",
    "Arabic 🇸🇦": "#34d399",
    "Hindi 🇮🇳": "#f472b6",
    "Spanish 🇪🇸": "#fb923c",
    "Russian 🇷🇺": "#a78bfa",
    "Japanese 🇯🇵": "#f87171",
    "Chinese 🇨🇳": "#60a5fa"
}

# --- Page Configuration ---
st.set_page_config(page_title="VocalNexus AI", layout="wide")

# --- Premium Design Engine (Inter & Montserrat Fonts + Dark Theme) ---
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
    h1, h2, h3, h4, label, p { color: #ffffff !important; }
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
        
        # Dynamic active voice badge
        accent_color = VOICE_DATA[selected_lang]
        st.markdown(f"<span style='background-color: {accent_color}20; color: {accent_color}; border: 1px solid {accent_color}; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;'>Active Model: {selected_lang}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Controls
        speed = st.slider("Speed (Tempo)", -50, 50, 0)
        pitch = st.slider("Pitch (Frequency)", -20, 20, 0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎙️ Compile & Synthesize"):
            st.success("Processing neural text matching sequence...")
            
    with col2:
        st.markdown("### Script Board")
        st.text_area("Workflow Sequence", height=280, placeholder="Enter your sequence narrative text here...")

elif st.session_state.page == 'About Us':
    st.markdown("## About VocalNexus AI")
    st.markdown("---")
    st.write("VocalNexus AI is a cutting-edge speech synthesis platform, meticulously engineered for creators who demand studio-grade neural audio. By bridging advanced deep-learning models with an intuitive workflow, we empower storytellers to transform text into captivating human-like narratives seamlessly.")

elif st.session_state.page == 'Privacy':
    st.markdown("## Privacy Policy")
    st.markdown("---")
    st.write("At VocalNexus AI, safeguarding your data is paramount. We implement industry-leading encryption standards to ensure that your scripts and metadata remain exclusively yours. We strictly adhere to a zero-retention policy for user-generated content unless explicitly opted-in for platform optimization.")

elif st.session_state.page == 'Terms':
    st.markdown("## Terms of Service")
    st.markdown("---")
    st.write("By accessing VocalNexus AI, you acknowledge that our services are provided for lawful, non-infringing use. Users maintain full ownership of all synthesized audio output. Unauthorized redistribution of our proprietary neural voice models is strictly prohibited under these Terms.")

elif st.session_state.page == 'Contact':
    st.markdown("## Contact Engineering Team")
    st.markdown("---")
    st.write("For enterprise inquiries, technical support, or system API integrations, our engineering team is available 24/7.")
    st.info("Global Support Email: support@vocalnexus.ai")

elif st.session_state.page == 'Disclaimer':
    st.markdown("## Legal Disclaimer")
    st.markdown("---")
    st.write("VocalNexus AI is an AI-augmented utility. While our neural synthesis achieves near-human parity, we cannot guarantee total contextual perfection in every generation. Users are responsible for the final review and legal compliance of all content created on this platform.")
