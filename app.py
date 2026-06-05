import streamlit as st

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'Studio'

# --- Page Config ---
st.set_page_config(page_title="VocalNexus AI", layout="wide")

# --- Premium Design Engine ---
css = """
<style>
    /* Premium Font Integration */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    h1, h2, h3 { font-family: 'Montserrat', sans-serif !important; font-weight: 700 !important; }
    
    .stApp { background-color: #030712 !important; }
    [data-testid="stSidebar"] { background-color: #0a0f1d !important; border-right: 1px solid #1e293b; }
    
    .stButton > button {
        border-radius: 8px !important;
        background: #1e293b !important;
        border: 1px solid #334155 !important;
        transition: all 0.3s ease;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🎙️ VocalNexus AI")
    st.divider()
    pages = ["Studio", "About Us", "Privacy", "Terms", "Contact", "Disclaimer"]
    for page in pages:
        if st.button(page, use_container_width=True):
            st.session_state.page = page
            st.rerun()

# --- Content Pages ---
if st.session_state.page == 'Studio':
    st.title("Studio Dashboard")
    # ... Your Studio UI Code ...

elif st.session_state.page == 'About Us':
    st.title("About VocalNexus AI")
    st.write("VocalNexus AI is a cutting-edge speech synthesis platform, meticulously engineered for creators who demand studio-grade neural audio. By bridging advanced deep-learning models with an intuitive workflow, we empower storytellers to transform text into captivating human-like narratives seamlessly.")

elif st.session_state.page == 'Privacy':
    st.title("Privacy Policy")
    st.write("At VocalNexus AI, safeguarding your data is paramount. We implement industry-leading encryption standards to ensure that your scripts and metadata remain exclusively yours. We strictly adhere to a zero-retention policy for user-generated content unless explicitly opted-in for platform optimization.")

elif st.session_state.page == 'Terms':
    st.title("Terms of Service")
    st.write("By accessing VocalNexus AI, you acknowledge that our services are provided for lawful, non-infringing use. Users maintain full ownership of all synthesized audio output. Unauthorized redistribution of our proprietary neural voice models is strictly prohibited under these Terms.")

elif st.session_state.page == 'Contact':
    st.title("Contact Us")
    st.write("For enterprise inquiries, technical support, or API integrations, our engineering team is available 24/7.")
    st.info("Email: support@vocalnexus.ai")

elif st.session_state.page == 'Disclaimer':
    st.title("Disclaimer")
    st.write("VocalNexus AI is an AI-augmented utility. While our neural synthesis achieves near-human parity, we cannot guarantee total contextual perfection in every generation. Users are responsible for the final review of all content created on this platform.")
