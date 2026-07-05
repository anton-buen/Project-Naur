import streamlit as st
import src.state_manager as sm
from src.engine import CognitiveAlignmentEngine

st.set_page_config(page_title="Cognitive Alignment Engine", layout="wide")

def apply_corporate_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono&display=swap');
        
        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Inter', sans-serif !important;
        }
        
        code, pre {
            font-family: 'JetBrains Mono', monospace !important;
        }

        .stButton>button {
            border-radius: 0px !important;
            background-color: #0f62fe !important;
            color: white !important;
            font-weight: 600;
            border: none;
            transition: background-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #0353e9 !important;
        }

        .stTextInput>div>div>input {
            border-radius: 0px !important;
            border: 1px solid #8d8d8d !important;
        }

        /* Custom Corporate Cards for Assumptions */
        .assumption-card {
            background-color: #f4f4f4;
            border-left: 4px solid #8a3ffc;
            padding: 1.5rem;
            margin-bottom: 1rem;
            height: 100%;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

apply_corporate_theme()

try:
    engine = CognitiveAlignmentEngine()
except Exception as e:
    st.error(f"System Failure: {e}")
    st.stop()

st.title("Cognitive Alignment Engine")
st.markdown("**Project Core:** Cross-Functional Assumption Extraction and Decompression")
st.markdown("---")

# Input Layer
with st.form("intent_form", clear_on_submit=True):
    user_intent = st.text_input("Enter the team's shared goal or intent...")
    submitted = st.form_submit_button("Extract Technical Assumptions")
    
    if submitted and user_intent:
        with st.spinner("Decompressing intent..."):
            engine.process_intent(user_intent)
        st.rerun()

# Output Layer
st.subheader("Extracted Constraints")
state = sm.read_state()
extractions = state.get("extractions", [])

if not extractions:
    st.caption("No intents processed yet.")
else:
    for item in reversed(extractions):
        st.markdown(f"**Intent:** {item['intent']}")
        assumptions = item.get('assumptions', {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='assumption-card'><strong>Frontend:</strong><br><br>{assumptions.get('FE', 'N/A')}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='assumption-card'><strong>Backend:</strong><br><br>{assumptions.get('BE', 'N/A')}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='assumption-card'><strong>Data Science:</strong><br><br>{assumptions.get('DS', 'N/A')}</div>", unsafe_allow_html=True)
        st.markdown("---")