import re
import streamlit as st
import src.state_manager as sm

st.set_page_config(page_title="Naur", layout="wide", initial_sidebar_state="expanded")

def apply_adaptive_theme():
    st.markdown("""
    <style>
        @font-face {
            font-family: 'SuisseIntl';
            src: url('SuisseIntl-Book.woff2') format('woff2');
            font-weight: normal;
            font-style: normal;
        }

        @media (prefers-color-scheme: light) {
            :root {
                --naur-accent-prod: #5D5D81;
                --naur-accent-fe: #6B4A3A;
                --naur-accent-be: #2F3E3E;
                --naur-accent-ds: #A3A08E;
                --naur-accent-ui: #9E768F;
                --naur-accent-risk: #C48A4A;
            }
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --naur-accent-prod: #5D5D81;
                --naur-accent-fe: #6B4A3A;
                --naur-accent-be: #2F3E3E;
                --naur-accent-ds: #A3A08E;
                --naur-accent-ui: #9E768F;
                --naur-accent-risk: #C48A4A;
            }
        }

        html, body, .stApp {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }

        h1, h2, h3 {
            font-weight: 500 !important;
            letter-spacing: -0.02em !important;
        }

        .subtext {
            opacity: 0.6;
            font-size: 0.9rem;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        
        [data-testid="stExpander"] summary p {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            font-size: 0.85rem !important;
        }

        [data-testid="stChatInput"] textarea {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-size: 1.05rem !important;
        }
        
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            padding: 0.5rem 0 !important;
        }
        
        .chat-human {
            background-color: rgba(128, 128, 128, 0.1);
            padding: 1rem 1.25rem;
            border-radius: 12px 12px 12px 2px;
            font-size: 0.95rem;
            line-height: 1.6;
            display: inline-block;
            border: 1px solid rgba(128, 128, 128, 0.2);
            color: inherit;
        }
        
        .chat-ai {
            background-color: transparent;
            padding: 1rem 1.25rem;
            border-radius: 12px 12px 2px 12px;
            font-size: 0.95rem;
            line-height: 1.6;
            opacity: 0.9;
            display: inline-block;
            border-left: 3px solid var(--naur-accent-risk);
            color: inherit;
        }

        .tech-card {
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            background-color: rgba(128, 128, 128, 0.05);
            font-size: 0.9rem;
            line-height: 1.6;
            height: 100%;
            color: inherit;
        }

        .card-prod { border-top: 4px solid var(--naur-accent-prod) !important; }
        .card-fe { border-top: 4px solid var(--naur-accent-fe) !important; }
        .card-be { border-top: 4px solid var(--naur-accent-be) !important; }
        .card-ds { border-top: 4px solid var(--naur-accent-ds) !important; }
        .card-ui { border-top: 4px solid var(--naur-accent-ui) !important; }
        
        .card-title {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            opacity: 0.7;
        }

        hr { border-color: rgba(128, 128, 128, 0.2) !important; margin: 2.5rem 0; }
        
        .risk-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 700;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-radius: 4px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .risk-high { 
            background-color: #B33A3A;
            color: #FFFFFF;
            border-left: 4px solid #FF8A8A;
        }
        .risk-medium { 
            background-color: #C48A4A;
            color: #111111;
            border-left: 4px solid #FFE0B2; 
        }
        .risk-low { 
            background-color: #4E6B4E;
            color: #FFFFFF;
            border-left: 4px solid #A5D6A7; 
        }
        
        .glossary-section {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-top: 4px solid var(--naur-accent-risk);
            background-color: rgba(128, 128, 128, 0.05);
            border-radius: 6px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            font-size: 0.9rem;
            color: inherit;
        }

        .glossary-title {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            margin-bottom: 1.25rem;
            opacity: 0.7;
        }
        
        .glossary-term {
            font-weight: 600;
            font-size: 0.9rem;
            margin-top: 1rem;
        }
        
        .glossary-definition {
            font-size: 0.9rem;
            line-height: 1.6;
            margin-top: 0.25rem;
            opacity: 0.8;
        }
        
        [data-testid="stChatInput"]::after {
            content: "Naur enforces team alignment. Verify constraints before implementation.";
            display: block;
            text-align: center;
            font-size: 0.75rem;
            opacity: 0.5;
            margin-top: 0.75rem;
            pointer-events: none;
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)

apply_adaptive_theme()

with st.sidebar:
    st.markdown("<h1 style='margin-bottom: 0.2rem; font-size: 1.5rem;'>Naur</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtext">Align your team before you build.</p>', unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Context</h3>", unsafe_allow_html=True)
    global_context = st.text_area(
        "Context",
        key="global_context",
        placeholder="e.g. AWS ECS. REST/JSON. Kafka.",
        height=120,
        label_visibility="collapsed",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Role</h3>", unsafe_allow_html=True)
    role = st.selectbox(
        "Role",
        options=["Product Manager", "Frontend Engineer", "Backend Engineer", "Data Scientist", "UI/UX Designer"],
        label_visibility="collapsed",
        key="active_role"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Admin</h3>", unsafe_allow_html=True)
    if st.button("Clear Chat", use_container_width=True):
        sm.clear_ledger()
        st.rerun()

st.markdown("<h2 style='margin-top: 0; font-size: 1.4rem;'>Discussion</h2>", unsafe_allow_html=True)
st.markdown('<p class="subtext">Identify blockers and define shared terms.</p>', unsafe_allow_html=True)

constraints = sm.get_constraints()
glossary = sm.get_glossary()

global_summary = constraints.pop("GLOBAL", None) if constraints else None

if constraints or global_summary:
    all_risks = list(constraints.values()) + ([global_summary] if global_summary else [])
    risk_priority = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}
    highest_risk = max(
        (v.get("risk", "LOW") for v in all_risks if isinstance(v, dict)),
        key=lambda r: risk_priority.get(r, 0),
        default="LOW"
    )
    
    risk_class = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(highest_risk, "risk-low")
    st.markdown(
        f"<div class='risk-badge {risk_class}'>Alignment Risk: {highest_risk}</div>",
        unsafe_allow_html=True
    )
    
    if global_summary:
        with st.expander("VIEW RISK RATIONALE", expanded=False):
            clean_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', global_summary.get("text", "No rationale provided."))
            st.markdown(f"<div style='font-size: 0.95rem; line-height: 1.6;'>{clean_text}</div>", unsafe_allow_html=True)

if constraints:
    with st.expander("DOMAIN CONSTRAINTS", expanded=True):
        domain_config = {
            "PROD": {"name": "Product", "class": "card-prod"},
            "FE": {"name": "Frontend", "class": "card-fe"},
            "BE": {"name": "Backend", "class": "card-be"},
            "DS": {"name": "Data Science", "class": "card-ds"},
            "UI": {"name": "UI/UX", "class": "card-ui"}
        }

        constraint_items = list(constraints.items())
        
        for i in range(0, len(constraint_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(constraint_items):
                    domain, data = constraint_items[i + j]
                    text = data.get("text", "No constraints detected.")
                    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                    conf = domain_config.get(domain, {"name": domain, "class": "card-be"})
                    
                    cols[j].markdown(
                        f"<div class='tech-card {conf['class']}'>"
                        f"<div class='card-title'>{conf['name']}</div>"
                        f"{text}</div>", 
                        unsafe_allow_html=True
                    )

if glossary:
    with st.expander("PROJECT DICTIONARY", expanded=False):
        terms_html = ""
        for term, definition in glossary.items():
            clean_def = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', definition)
            clean_def = clean_def.replace("In Project Naur, ", "").replace("Project Naur", "This project")
            
            terms_html += (
                f"<div class='glossary-term'>{term}</div>"
                f"<div class='glossary-definition'>{clean_def}</div>"
            )
            
        st.markdown(
            f"<div class='glossary-section'>"
            f"{terms_html}"
            f"</div>",
            unsafe_allow_html=True
        )
    
st.markdown("<hr>", unsafe_allow_html=True)

thread = sm.get_chat_history()

for msg in thread:
    clean_content = re.sub(r' \[Context: .*?\]', '', msg["content"])
        
    if msg["role"] == "human":
        avatar_initials = "U"
        if "[Product" in clean_content: avatar_initials = "PM"
        elif "[Frontend" in clean_content: avatar_initials = "FE"
        elif "[Backend" in clean_content: avatar_initials = "BE"
        elif "[Data" in clean_content: avatar_initials = "DS"
        elif "[UI" in clean_content: avatar_initials = "UI"

        avatar_url = f"https://ui-avatars.com/api/?name={avatar_initials}&background=2A2A2A&color=E9DDCF&rounded=true&bold=true&font-size=0.4"

        with st.chat_message("human", avatar=avatar_url):
            st.markdown(f"<div class='chat-human'>{clean_content}</div>", unsafe_allow_html=True)
            
    elif msg["role"] == "assistant":
        naur_avatar = "https://ui-avatars.com/api/?name=N&background=C48A4A&color=111111&rounded=true&bold=true"
        
        with st.chat_message("assistant", avatar=naur_avatar):
            st.markdown(f"<div class='chat-ai'>{clean_content}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

if user_intent := st.chat_input("Join the discussion..."):
    active_role = st.session_state.get("active_role", "Product Manager")
    stamped_intent = f"[{active_role}] {user_intent}"

    global_context = st.session_state.get("global_context", "").strip()
    if global_context:
        stamped_intent += f" [Context: {global_context}]"

    sm.append_message("human", stamped_intent)
    st.rerun()