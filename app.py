import streamlit as st

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'Studio'

# --- Configuration ---
st.set_page_config(page_title="VocalForge Studio", layout="wide")

# --- UI Styling ---
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0f172a !important; }
    .stApp { background-color: #030712 !important; }
    h1, h2, h3, label { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("VocalForge Studio")
    st.markdown("---")
    pages = ["Studio", "About Us", "Privacy", "Terms", "Contact", "Disclaimer"]
    for page in pages:
        if st.button(page, use_container_width=True):
            st.session_state.page = page
            st.rerun()

# --- Page Content Router ---
if st.session_state.page == 'Studio':
    st.title("🎙️ Studio Dashboard")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.selectbox("Select Language", ["English 🇺🇸", "Urdu 🇵🇰", "Arabic 🇸🇦"])
        st.slider("Speed", -50, 50, 0)
        st.slider("Pitch", -20, 20, 0)
        st.button("COMPILE & SYNTHESIZE")
    with col2:
        st.text_area("Workflow", height=200, placeholder="Enter your text here...")

elif st.session_state.page == 'About Us':
    st.title("About Us")
    st.write("VocalForge Studio is a professional AI voice solution designed for modern content creators to save production time while maintaining premium audio quality using Neural TTS technology.")

elif st.session_state.page == 'Privacy':
    st.title("Privacy Policy")
    st.write("• **Data Collection**: We collect minimal data to improve user experience.\n• **Security**: Your data is encrypted and stored securely.\n• **Sharing**: We do not share personal data with third parties.")

elif st.session_state.page == 'Terms':
    st.title("Terms of Service")
    st.write("• **Usage**: Use this tool for legal and ethical purposes only.\n• **Ownership**: You retain the rights to the content generated.\n• **Modifications**: We reserve the right to update our services at any time.")

elif st.session_state.page == 'Contact':
    st.title("Contact Us")
    st.write("• **Email**: support@vocalforge.studio\n• **Support**: Our team typically responds within 24 hours.")

elif st.session_state.page == 'Disclaimer':
    st.title("Disclaimer")
    st.write("• **Accuracy**: AI-generated audio is provided 'as-is'; perfect accuracy cannot be guaranteed.\n• **Liability**: Users are solely responsible for the content generated and its application.")
