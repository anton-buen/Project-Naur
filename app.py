import streamlit as st
import src.state_manager as sm

st.set_page_config(page_title="Naur", layout="wide", initial_sidebar_state="expanded")

def apply_adaptive_theme():
    """Inject global CSS: SuisseIntl typography, domain card accents, and chat interface styles."""
    st.markdown("""
    <style>
        @font-face {
            font-family: 'SuisseIntl';
            src: url('SuisseIntl-Book.woff2') format('woff2');
            font-weight: normal;
            font-style: normal;
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

        [data-testid="stChatInput"] textarea {
            font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace !important;
            font-size: 1.05rem !important;
        }
        [data-testid="stChatMessage"] {
            font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace !important;
            font-size: 0.92rem !important;
            line-height: 1.7 !important;
        }

        .tech-card {
            padding: 1.5rem;
            border-radius: 6px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            background-color: rgba(128, 128, 128, 0.03);
            font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace !important;
            font-size: 0.9rem;
            line-height: 1.6;
            height: 100%;
        }
        
        .card-fe { border-top: 4px solid #6B4A3A !important; }
        .card-be { border-top: 4px solid #2F3E3E !important; }
        .card-ds { border-top: 4px solid #A3A08E !important; }
        
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
            padding: 0.4rem 0.8rem;
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-radius: 4px;
            margin-bottom: 1.5rem;
            border-left: 4px solid #C48A4A;
            background-color: rgba(196, 138, 74, 0.1); 
        }
        .risk-high {
            border-left-color: #6B4A3A;
            background-color: rgba(107, 74, 58, 0.15);
        }
        
        .glossary-section {
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-top: 4px solid #C48A4A;
            background-color: rgba(128, 128, 128, 0.03);
            border-radius: 6px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace !important;
            font-size: 0.9rem;
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

def generate_markdown_export(intent: str, assumptions: dict) -> str:
    risk = assumptions.get('risk_score', 'N/A')
    blockers = assumptions.get('blockers', 'None identified.')
    glossary = assumptions.get('dictionary', {})
    glossary_md = "\n".join([f"- **{k}:** {v}" for k, v in glossary.items()]) or "None."
    return (
        f"# Alignment Extraction\n"
        f"**Intent:** {intent}\n\n"
        f"**Alignment Risk Score:** {risk}\n\n"
        f"### Technical Constraints\n"
        f"- **Frontend:** {assumptions.get('FE', 'None detected.')}\n"
        f"- **Backend:** {assumptions.get('BE', 'None detected.')}\n"
        f"- **Data Science:** {assumptions.get('DS', 'None detected.')}\n\n"
        f"### Critical Blockers\n{blockers}\n\n"
        f"### Glossary\n{glossary_md}\n"
    )

apply_adaptive_theme()

with st.sidebar:
    st.markdown("<h1 style='margin-bottom: 0.2rem; font-size: 1.5rem;'>Naur</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtext">Align your team before you build.</p>', unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--naur-muted) !important;'>Context</h3>", unsafe_allow_html=True)
    global_context = st.text_area(
        "Context",
        key="global_context",
        placeholder="e.g. AWS ECS. REST/JSON. Kafka.",
        height=120,
        label_visibility="collapsed",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--naur-muted) !important;'>Role</h3>", unsafe_allow_html=True)
    role = st.selectbox(
        "Role",
        options=["Product Manager", "Frontend Engineer", "Backend Engineer", "Data Scientist", "UI/UX Designer"],
        label_visibility="collapsed",
        key="active_role"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--naur-muted) !important;'>Admin</h3>", unsafe_allow_html=True)
    if st.button("Clear Chat", use_container_width=True):
        sm.clear_ledger()
        st.rerun()

st.markdown("<h2 style='margin-top: 0; font-size: 1.4rem;'>Discussion</h2>", unsafe_allow_html=True)
st.markdown('<p class="subtext">Identify blockers and define shared terms.</p>', unsafe_allow_html=True)

constraints = sm.get_constraints()
glossary = sm.get_glossary()

if constraints or glossary:
    risk_priority = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}
    highest_risk = max(
        (v["risk"] for v in constraints.values() if v.get("risk") in risk_priority),
        key=lambda r: risk_priority.get(r, 0),
        default="LOW"
    )
    risk_class = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(highest_risk, "risk-low")
    st.markdown(
        f"<div class='risk-badge {risk_class}'>Alignment Risk: {highest_risk}</div>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        fe = constraints.get("FE", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card'><div class='card-title'>Frontend</div>{fe}</div>", unsafe_allow_html=True)
    with col2:
        be = constraints.get("BE", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card'><div class='card-title'>Backend</div>{be}</div>", unsafe_allow_html=True)
    with col3:
        ds = constraints.get("DS", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card'><div class='card-title'>Data Science</div>{ds}</div>", unsafe_allow_html=True)

    if glossary:
        terms_html = "".join([
            f"<div class='glossary-term'>{term}</div>"
            f"<div class='glossary-definition'>{definition}</div>"
            for term, definition in glossary.items()
        ])
        st.markdown(
            f"<div class='glossary-section'>"
            f"<div class='glossary-title'>Glossary</div>"
            f"{terms_html}"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)

thread = sm.get_chat_history()

if not thread:
    st.markdown("<div style='color: var(--naur-muted); font-size: 0.9rem; margin-top: 1rem;'>No discussion logged. Propose a feature below.</div>", unsafe_allow_html=True)
else:
    for msg in thread:
        if msg["role"] == "human":
            with st.chat_message("human"):
                st.markdown(f"<div style='font-weight: 500; font-size: 1.05rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(f"<div style='color: var(--naur-muted);'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

if user_intent := st.chat_input("Join the discussion..."):
    active_role = st.session_state.get("active_role", "Product Manager")
    stamped_intent = f"[{active_role}] {user_intent}"

    global_context = st.session_state.get("global_context", "").strip()
    if global_context:
        stamped_intent += f" [Context: {global_context}]"

    sm.append_message("human", stamped_intent)
    st.rerun()