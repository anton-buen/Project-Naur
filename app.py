import streamlit as st
import src.state_manager as sm

# 1. UI Configuration
st.set_page_config(page_title="Project Naur", layout="wide", initial_sidebar_state="expanded")

def apply_adaptive_theme():
    """
    Bulletproof fluid theming. 
    Pins the disclaimer to the bottom viewport and elevates the chat input.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* 1. Define Strict Palette Variables */
        @media (prefers-color-scheme: light) {
            :root {
                --naur-bg: #FBF9F5;
                --naur-surface: #F2EFE9;
                --naur-text: #1E1D1B;
                --naur-border: #E2DCD2;
                --naur-muted: #68645E;
            }
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --naur-bg: #161616;
                --naur-surface: #262626;
                --naur-text: #f4f4f4;
                --naur-border: #393939;
                --naur-muted: #8d8d8d;
            }
        }

        /* 2. Bruteforce Backgrounds */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: var(--naur-bg) !important;
            color: var(--naur-text) !important;
            font-family: 'IBM Plex Sans', sans-serif !important;
        }
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
            background-color: var(--naur-surface) !important;
        }

        /* 3. Typography Management */
        .naur-header { font-family: 'IBM Plex Sans', sans-serif !important; font-weight: 600; color: var(--naur-text) !important; }
        h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif !important; color: var(--naur-text) !important; }
        [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * { color: var(--naur-text) !important; }

        /* 4. Chat Interface Overrides */
        [data-testid="stChatInput"] {
            background-color: var(--naur-bg) !important;
            padding-bottom: 3rem !important; 
        }
        [data-testid="stChatInput"] textarea {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.05rem !important;
            background-color: var(--naur-surface) !important;
            border: 1px solid var(--naur-border) !important;
            border-radius: 0px !important;
            color: var(--naur-text) !important;
            padding: 1rem !important;
        }
        [data-testid="stChatInput"] textarea:focus { border-color: var(--naur-text) !important; }
        
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
            border-radius: 0px !important;
            padding: 1.5rem 0 !important;
            border-bottom: 1px solid var(--naur-border);
        }
        [data-testid="chatAvatarIcon-human"], [data-testid="chatAvatarIcon-user"] {
            background-color: var(--naur-surface) !important;
            color: var(--naur-text) !important;
            border: 1px solid var(--naur-border);
            border-radius: 0px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }
        [data-testid="chatAvatarIcon-assistant"] {
            background-color: var(--naur-text) !important;
            color: var(--naur-bg) !important;
            border-radius: 0px !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 5. Buttons */
        .stButton>button, .stDownloadButton>button {
            border-radius: 0px !important;
            font-family: 'IBM Plex Sans', sans-serif !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.8rem !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.2s ease !important;
            background-color: transparent !important;
            border: 1px solid var(--naur-border) !important;
            color: var(--naur-text) !important;
        }
        .stDownloadButton>button:hover, [data-testid="stSidebar"] .stButton>button:hover {
            border-color: var(--naur-text) !important;
        }

        /* 6. Output Cards */
        .tech-card {
            background-color: var(--naur-surface);
            border: 1px solid var(--naur-border);
            padding: 1.5rem;
            height: 100%;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem;
            line-height: 1.6;
            color: var(--naur-text);
            white-space: pre-wrap;
        }
        .card-title {
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
        }
        /* Card body text uses mono; only the title is IBM Plex Sans */
        .tech-card { font-family: 'JetBrains Mono', monospace !important; }
        .card-fe { border-top: 3px solid #78a9ff !important; } 
        .card-be { border-top: 3px solid #42be65 !important; } 
        .card-ds { border-top: 3px solid #be95ff !important; } 

        hr { border-color: var(--naur-border) !important; margin: 2.5rem 0; }
        
        /* Risk Score Badge */
        .risk-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border-radius: 0px;
            margin-bottom: 1.5rem;
        }
        .risk-high { background-color: #da1e28; color: #ffffff; }
        .risk-medium { background-color: #f1c21b; color: #161616; }
        .risk-low { background-color: #24a148; color: #ffffff; }
        
        /* Blockers Warning Banner */
        .blockers-banner {
            background-color: var(--naur-surface);
            border-left: 4px solid #da1e28;
            padding: 1.25rem;
            margin: 1.5rem 0;
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        .blockers-title {
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            margin-bottom: 0.75rem;
            color: #da1e28;
        }
        
        /* Glossary Section */
        .glossary-section {
            background-color: var(--naur-surface);
            border: 1px solid var(--naur-border);
            padding: 1.5rem;
            margin: 1.5rem 0;
            font-family: 'IBM Plex Sans', sans-serif;
        }
        .glossary-title {
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            margin-bottom: 1rem;
            color: var(--naur-text);
        }
        .glossary-term {
            font-weight: 600;
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.85rem;
            margin-top: 0.75rem;
            color: var(--naur-text);
        }
        .glossary-definition {
            font-size: 0.85rem;
            line-height: 1.6;
            margin-top: 0.25rem;
            opacity: 0.9;
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* 7. Permanent Fixed Footer */
        [data-testid="stChatInput"] {
            padding-bottom: 2rem !important; 
        }
        
        [data-testid="stChatInput"]::after {
            content: "Project Naur helps catch technical blind spots before coding begins. AI can make mistakes, so always review these constraints with your team.";
            display: block;
            text-align: center;
            font-size: 0.75rem;
            color: var(--naur-muted);
            font-family: 'IBM Plex Sans', sans-serif;
            margin-top: 0.5rem;
            opacity: 0.8;
            pointer-events: none;
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
        f"### Ontological Glossary\n{glossary_md}\n"
    )

# 2. Inject Theme
apply_adaptive_theme()

# 3. Sidebar
with st.sidebar:
    st.markdown("<h2 class='naur-header' style='margin-bottom: 0.5rem; font-size: 1.6rem;'>Project Naur</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.9rem; margin-bottom: 2rem; opacity: 0.8;'>Decompress feature intents to prevent integration failure.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Global Team Context</h3>", unsafe_allow_html=True)
    global_context = st.text_area(
        "Global Team Context",
        key="global_context",
        placeholder="e.g. We use AWS ECS. Our API contract is REST/JSON. All events go through Kafka.",
        help="Paste your company's existing definitions or architecture rules here so the AI respects them.",
        height=120,
        label_visibility="collapsed",
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Active Role</h3>", unsafe_allow_html=True)
    role = st.selectbox(
        "Select your role:",
        options=["Product Manager", "Frontend Engineer", "Backend Engineer", "Data Scientist", "UI/UX Designer"],
        label_visibility="collapsed",
        key="active_role"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Session Admin</h3>", unsafe_allow_html=True)
    if st.button("Clear Ledger", use_container_width=True):
        sm.clear_ledger()
        st.rerun()

# 5. Cross-Functional Alignment Thread
st.markdown("<h2 class='naur-header' style='margin-top: 0; font-size: 1.5rem;'>Cross-Functional Alignment Thread</h2>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.85rem; opacity: 0.6; margin-top: -0.75rem; margin-bottom: 1.5rem;'>Identifies integration blockers before the sprint begins.</p>", unsafe_allow_html=True)

# --- Global Alignment Dashboard ---
constraints = sm.get_constraints()
glossary = sm.get_glossary()

if constraints or glossary:
    # Derive highest risk level across all domains
    risk_priority = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}
    highest_risk = max(
        (v["risk"] for v in constraints.values() if v.get("risk") in risk_priority),
        key=lambda r: risk_priority.get(r, 0),
        default="LOW"
    )
    risk_class = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(highest_risk, "risk-low")
    st.markdown(
        f"<div class='risk-badge {risk_class}'>&#9632; Alignment Risk: {highest_risk}</div>",
        unsafe_allow_html=True
    )

    # --- Domain Constraint Cards ---
    col1, col2, col3 = st.columns(3)
    with col1:
        fe = constraints.get("FE", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card card-fe'><div class='card-title' style='color: #78a9ff;'>Frontend Requirements</div>{fe}</div>", unsafe_allow_html=True)
    with col2:
        be = constraints.get("BE", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card card-be'><div class='card-title' style='color: #42be65;'>Backend Requirements</div>{be}</div>", unsafe_allow_html=True)
    with col3:
        ds = constraints.get("DS", {}).get("text", "No constraints detected.")
        st.markdown(f"<div class='tech-card card-ds'><div class='card-title' style='color: #be95ff;'>Data Science Requirements</div>{ds}</div>", unsafe_allow_html=True)

    # --- Project Dictionary ---
    if glossary:
        terms_html = "".join([
            f"<div class='glossary-term'>{term}</div>"
            f"<div class='glossary-definition'>{definition}</div>"
            for term, definition in glossary.items()
        ])
        st.markdown(
            f"<div class='glossary-section'>"
            f"<div class='glossary-title'>&#9679; Project Dictionary "
            f"<span title='Agreed-upon definitions to prevent miscommunication.' style='cursor: help;'>&#8505;</span>"
            f"</div>"
            f"{terms_html}"
            f"</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)

# --- Chat History ---
thread = sm.get_chat_history()

if not thread:
    st.markdown("<div style='opacity: 0.6; margin-top: 1rem;'>The thread is empty. Propose a feature below to begin alignment.</div>", unsafe_allow_html=True)
else:
    for msg in thread:
        if msg["role"] == "human":
            with st.chat_message("human"):
                st.markdown(f"<div style='font-weight: 600; font-size: 1.05rem;'>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"], unsafe_allow_html=True)

# Padding
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# 6. Chat Input Layer
if user_intent := st.chat_input("Join the discussion... (e.g., 'We can't use WebSockets...')"):
    # Prepend the active role to contextualise the message for the engine
    active_role = st.session_state.get("active_role", "Product Manager")
    stamped_intent = f"[{active_role}] {user_intent}"

    # Append global team context if provided
    global_context = st.session_state.get("global_context", "").strip()
    if global_context:
        stamped_intent += f" [Team Context: {global_context}]"

    sm.append_message("human", stamped_intent)
    st.rerun()