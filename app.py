import re
import streamlit as st
import src.state_manager as sm
from datetime import datetime

st.set_page_config(page_title="Naur", layout="wide", initial_sidebar_state="expanded")


def parse_markdown(text: str) -> str:
    """Convert a limited Markdown subset to HTML.

    Handles bold, italic, inline code, headings (h1–h3), unordered and
    ordered lists, and pipe-delimited tables.  Returns an empty string
    when *text* is falsy or the literal string ``"none"``.

    Args:
        text: Raw Markdown string to convert.

    Returns:
        An HTML string suitable for use with ``unsafe_allow_html=True``.
    """
    if not text or str(text).strip().lower() == "none":
        return ""

    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(
        r'`([^`]+)`',
        r'<code style="background: rgba(128,128,128,0.2); padding: 2px 4px; '
        r'border-radius: 4px; font-family: monospace; font-size: 0.85em;">\1</code>',
        text,
    )

    lines = text.split('\n')
    parsed = []
    in_ul, in_ol, in_table, is_first_table_row = False, False, False, False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("|") and stripped.endswith("|"):
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if in_ol:
                parsed.append("</ol>")
                in_ol = False

            if not in_table:
                parsed.append(
                    "<div style='overflow-x: auto;'><table style='width: 100%; border-collapse: collapse; "
                    "margin: 1rem 0; font-size: 0.85rem; text-align: left; border: 1px solid rgba(128,128,128,0.2);'>"
                )
                in_table = True
                is_first_table_row = True

            if re.match(r'^\|[\s\-\|]+\|$', stripped):
                is_first_table_row = False
                continue

            cells = [cell.strip() for cell in stripped.strip('|').split('|')]
            parsed.append("<tr style='border-bottom: 1px solid rgba(128,128,128,0.1);'>")
            for cell in cells:
                if is_first_table_row:
                    parsed.append(
                        f"<th style='padding: 0.75rem; font-weight: 600; background: rgba(128,128,128,0.05); "
                        f"border-right: 1px solid rgba(128,128,128,0.1);'>{cell}</th>"
                    )
                else:
                    parsed.append(
                        f"<td style='padding: 0.75rem; border-right: 1px solid rgba(128,128,128,0.1);'>{cell}</td>"
                    )
            parsed.append("</tr>")
            is_first_table_row = False
            continue
        else:
            if in_table:
                parsed.append("</table></div>")
                in_table = False

        if stripped.startswith("### "):
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if in_ol:
                parsed.append("</ol>")
                in_ol = False
            parsed.append(f"<h5 style='margin-top: 1rem; margin-bottom: 0.5rem; opacity: 0.9;'>{stripped[4:]}</h5>")
            continue
        elif stripped.startswith("## "):
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if in_ol:
                parsed.append("</ol>")
                in_ol = False
            parsed.append(f"<h4 style='margin-top: 1rem; margin-bottom: 0.5rem; opacity: 0.9;'>{stripped[3:]}</h4>")
            continue
        elif stripped.startswith("# "):
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if in_ol:
                parsed.append("</ol>")
                in_ol = False
            parsed.append(f"<h3 style='margin-top: 1rem; margin-bottom: 0.5rem; opacity: 0.9;'>{stripped[2:]}</h3>")
            continue

        if stripped.startswith("- "):
            if in_ol:
                parsed.append("</ol>")
                in_ol = False
            if not in_ul:
                parsed.append("<ul style='margin: 0.5rem 0; padding-left: 1.5rem;'>")
                in_ul = True
            parsed.append(f"<li style='margin-bottom: 0.25rem;'>{stripped[2:]}</li>")
        elif re.match(r'^\d+\.\s', stripped):
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if not in_ol:
                parsed.append("<ol style='margin: 0.5rem 0; padding-left: 1.5rem;'>")
                in_ol = True
            content = re.sub(r'^\d+\.\s', '', stripped)
            parsed.append(f"<li style='margin-bottom: 0.25rem;'>{content}</li>")
        elif stripped:
            if in_ul:
                parsed.append("</ul>")
                in_ul = False
            if in_ol:
                parsed.append("</ol>")
                in_ol = False
            parsed.append(f"<div style='margin-bottom: 0.75rem; line-height: 1.6;'>{stripped}</div>")

    if in_ul:
        parsed.append("</ul>")
    if in_ol:
        parsed.append("</ol>")
    if in_table:
        parsed.append("</table></div>")

    return "".join(parsed)


def apply_adaptive_theme() -> None:
    """Inject the application's global CSS into the Streamlit page.

    Registers the SuisseIntl font, CSS custom properties for domain accent
    colours, and all component-level styles (cards, badges, chat bubbles,
    expanders, glossary).  Must be called once at startup before any other
    ``st.*`` calls render content.
    """
    st.markdown("""
    <style>
        @font-face { font-family: 'SuisseIntl'; src: url('SuisseIntl-Book.woff2') format('woff2'); font-weight: normal; font-style: normal; }
        
        :root {
            --naur-accent-prod: #5D5D81; --naur-accent-fe: #6B4A3A; --naur-accent-be: #2F3E3E;
            --naur-accent-ds: #A3A08E; --naur-accent-ui: #9E768F; --naur-accent-risk: #C48A4A;
        }

        html, body, .stApp { font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }
        h1, h2, h3 { font-weight: 500 !important; letter-spacing: -0.02em !important; }
        
        .brand-title {
            font-family: 'Charter', 'Palatino Linotype', 'Book Antiqua', Palatino, serif !important;
            font-size: 2.6rem !important; font-weight: 700 !important; margin-bottom: 0 !important;
            letter-spacing: -0.03em !important; color: var(--naur-accent-risk);
        }

        .subtext { opacity: 0.6; font-size: 0.9rem; margin-top: -5px; margin-bottom: 15px; }
        
        [data-testid="stChatInput"] textarea, [data-testid="stTextArea"] textarea { 
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important; 
            font-size: 0.9rem !important; 
        }

        div[data-testid="stButton"] button {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600 !important; text-transform: uppercase !important;
            letter-spacing: 0.05em !important; font-size: 0.75rem !important;
            border-radius: 4px !important; padding: 0.35rem 0.5rem !important; min-height: 0 !important;
        }

        [data-testid="stExpander"] { border: none !important; box-shadow: none !important; background: transparent !important; }
        [data-testid="stExpander"] summary {
            background-color: rgba(128,128,128,0.03) !important; border-radius: 6px !important;
            padding: 0.75rem 1rem !important; margin-bottom: 0.5rem !important;
            border: 1px solid rgba(128,128,128,0.1) !important;
        }
        [data-testid="stExpander"] summary p {
            font-family: 'SuisseIntl', 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            font-weight: 600 !important; text-transform: uppercase !important;
            letter-spacing: 0.05em !important; font-size: 0.85rem !important; opacity: 0.8 !important;
            margin: 0 !important; padding: 0 !important;
        }
        
        [data-testid="stChatMessage"] { background-color: transparent !important; padding: 0.5rem 0 !important; }
        
        .chat-human { background-color: rgba(128, 128, 128, 0.1); padding: 1rem 1.25rem; border-radius: 12px 12px 12px 2px; font-size: 0.95rem; line-height: 1.6; display: inline-block; border: 1px solid rgba(128, 128, 128, 0.2); color: inherit; }
        .chat-ai { background-color: transparent; padding: 1rem 1.25rem; border-radius: 12px 12px 2px 12px; font-size: 0.95rem; line-height: 1.6; opacity: 0.9; display: inline-block; border-left: 3px solid var(--naur-accent-risk); color: inherit; }

        .header-container { display: flex; align-items: center; gap: 12px; margin-bottom: 1rem; flex-wrap: wrap; }
        .risk-badge { padding: 0.5rem 1rem; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .risk-high { background-color: #B33A3A; color: #FFFFFF; border-left: 4px solid #FF8A8A; }
        .risk-medium { background-color: #C48A4A; color: #111111; border-left: 4px solid #FFE0B2; }
        .risk-low { background-color: #4E6B4E; color: #FFFFFF; border-left: 4px solid #A5D6A7; }
        
        .mini-blast {
            padding: 0.2rem 0.5rem; font-weight: 700; font-size: 0.65rem; text-transform: uppercase;
            letter-spacing: 0.05em; border-radius: 4px; cursor: help;
            box-shadow: 0 1px 2px rgba(0,0,0,0.15);
        }
        .mini-HIGH { background-color: #B33A3A; color: #FFFFFF; }
        .mini-MEDIUM { background-color: #C48A4A; color: #111111; }
        .mini-LOW { background-color: #4E6B4E; color: #FFFFFF; }

        .tech-card { padding: 1.5rem; border-radius: 6px; border: 1px solid rgba(128, 128, 128, 0.2); background-color: rgba(128, 128, 128, 0.05); font-size: 0.9rem; line-height: 1.6; height: 100%; color: inherit; display: flex; flex-direction: column; }
        .card-prod { border-top: 4px solid var(--naur-accent-prod) !important; }
        .card-fe { border-top: 4px solid var(--naur-accent-fe) !important; }
        .card-be { border-top: 4px solid var(--naur-accent-be) !important; }
        .card-ds { border-top: 4px solid var(--naur-accent-ds) !important; }
        .card-ui { border-top: 4px solid var(--naur-accent-ui) !important; }
        
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid rgba(128,128,128,0.1); padding-bottom: 0.5rem; }
        .card-title { font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.75rem; opacity: 0.8; margin: 0; }

        .jargon-toggle { display: none; }
        .jargon-label { font-size: 0.65rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; cursor: pointer; padding: 4px 8px; border-radius: 4px; background: rgba(128, 128, 128, 0.1); border: 1px solid rgba(128, 128, 128, 0.3); transition: 0.2s; user-select: none; }
        .jargon-label:hover { background: rgba(128, 128, 128, 0.2); }
        .jargon-toggle:checked ~ .card-header .jargon-label { background: var(--naur-accent-risk); color: #111; border-color: transparent; }
        
        .biz-text { display: none; font-size: 0.95rem; padding-top: 0.5rem; flex-grow: 1; }
        .tech-text { display: block; font-size: 0.9rem; padding-top: 0.5rem; flex-grow: 1; }
        .jargon-toggle:checked ~ .tech-text { display: none; }
        .jargon-toggle:checked ~ .biz-text { display: block; }

        details.deep-dive { margin-top: 1.5rem; border-radius: 4px; border: 1px solid rgba(128, 128, 128, 0.2); overflow: hidden; background: rgba(0,0,0,0.1); }
        details.deep-dive summary { padding: 0.75rem; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; cursor: pointer; outline: none; transition: background 0.2s; list-style: none; text-align: center; opacity: 0.8;}
        details.deep-dive summary::-webkit-details-marker { display: none; }
        details.deep-dive summary:hover { background: rgba(128, 128, 128, 0.1); opacity: 1; }
        details.deep-dive .deep-content { padding: 1rem; font-size: 0.85rem; line-height: 1.6; border-top: 1px solid rgba(128, 128, 128, 0.2); opacity: 0.9; }

        hr { border-color: rgba(128, 128, 128, 0.2) !important; margin: 2.5rem 0; }
        .glossary-section { border: 1px solid rgba(128, 128, 128, 0.2); border-top: 4px solid var(--naur-accent-risk); background-color: rgba(128, 128, 128, 0.05); border-radius: 6px; padding: 1.5rem; margin: 0.5rem 0; font-size: 0.9rem; color: inherit; }
        .glossary-term { font-weight: 600; font-size: 0.9rem; margin-top: 1rem; }
        .glossary-definition { font-size: 0.9rem; line-height: 1.6; margin-top: 0.25rem; opacity: 0.8; }
        
        [data-testid="stChatInput"]::after { content: "Naur enforces team alignment. Check your constraints before you code."; display: block; text-align: center; font-size: 0.75rem; opacity: 0.5; margin-top: 0.75rem; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)


apply_adaptive_theme()

with st.sidebar:
    st.markdown("<h1 class='brand-title'>Naur</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtext">Align your team, skip the friction.</p>', unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7; margin-top: 1rem;'>Role</h3>", unsafe_allow_html=True)
    role = st.selectbox("Role", options=["Product Manager", "Frontend Engineer", "Backend Engineer", "Data Scientist", "UI/UX Designer"], label_visibility="collapsed", key="active_role")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Context</h3>", unsafe_allow_html=True)
    global_context = st.text_area("Context", key="global_context", placeholder="e.g. Serverless AWS. HIPAA Compliance. React Native.", height=120, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Governance</h3>", unsafe_allow_html=True)
    gov_phase = st.select_slider("Governance", options=["Ideation", "Architecture", "Pre-Flight"], value="Architecture", label_visibility="collapsed")

    st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.7;'>Actions</h3>", unsafe_allow_html=True)
    st.markdown('<p style="font-size: 0.75rem; opacity: 0.6; line-height: 1.4; margin-bottom: 12px;">Naur silently checks your blind spots. Sync to see the latest insights.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sync", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Clear", use_container_width=True):
            sm.clear_ledger()
            st.rerun()

current_date = datetime.now().strftime("%A, %b %d, %Y")

st.markdown(f"""
<div style="margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(128,128,128,0.2); display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
        <h2 style='margin-top: 0; margin-bottom: 0.25rem; font-size: 1.5rem;'>ProjectName_1</h2>
        <p class="subtext" style="margin-bottom: 0;">Your message here: clarify + identify</p>
    </div>
    <div style="text-align: right;">
        <div style="font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; opacity: 0.5;">Session Date</div>
        <div style="font-size: 0.85rem; font-weight: 500; opacity: 0.8;">{current_date}</div>
    </div>
</div>
""", unsafe_allow_html=True)

constraints = sm.get_constraints()
glossary = sm.get_glossary()

global_summary = constraints.pop("GLOBAL", None) if constraints else None
active_domains = list(constraints.keys())

if constraints or global_summary:
    all_risks = list(constraints.values()) + ([global_summary] if global_summary else [])
    risk_priority = {"HIGH": 2, "MEDIUM": 1, "LOW": 0}
    highest_risk = max(
        (v.get("risk", "LOW") for v in all_risks if isinstance(v, dict)),
        key=lambda r: risk_priority.get(r, 0),
        default="LOW",
    )

    risk_hex_map = {"HIGH": "#B33A3A", "MEDIUM": "#C48A4A", "LOW": "#4E6B4E"}
    risk_color_hex = risk_hex_map.get(highest_risk, "#C48A4A")
    risk_class = {"HIGH": "risk-high", "MEDIUM": "risk-medium", "LOW": "risk-low"}.get(highest_risk, "risk-low")

    header_html = f"<div class='header-container'><div class='risk-badge {risk_class}'>Alignment Risk: {highest_risk}</div>"
    if active_domains:
        header_html += "<div style='display: flex; gap: 6px; align-items: center; border-left: 1px solid rgba(128,128,128,0.2); padding-left: 12px; margin-left: 4px;'>"
        header_html += "<span style='font-size: 0.65rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; opacity: 0.5;'>Blast Radius:</span>"
        for dom in active_domains:
            dom_risk = constraints[dom].get("risk", "LOW")
            header_html += f"<div class='mini-blast mini-{dom_risk}' title='{dom} Risk: {dom_risk}'>{dom}</div>"
        header_html += "</div>"
    header_html += "</div>"
    st.markdown(header_html, unsafe_allow_html=True)

    if global_summary:
        with st.expander("RATIONALE", expanded=False):
            tech_text = parse_markdown(global_summary.get("text", ""))
            biz_text = parse_markdown(global_summary.get("business", ""))
            deep_dive = parse_markdown(global_summary.get("deep_dive", ""))

            deep_dive_html = (
                f"<details class='deep-dive'><summary>Deep Dive</summary><div class='deep-content'>{deep_dive}</div></details>"
                if deep_dive else ""
            )

            summary_html = f"""
            <div class='tech-card' style='border-top: 4px solid {risk_color_hex};'>
                <input type='checkbox' id='toggle-global' class='jargon-toggle'>
                <div class='card-header'>
                    <div class='card-title'>Global Summary</div>
                    <label for='toggle-global' class='jargon-label'>Translate</label>
                </div>
                <div class='tech-text'><b>Critical Blockers:</b><br>{tech_text}</div>
                <div class='biz-text'><b>Velocity Impact:</b><br>{biz_text}</div>
                {deep_dive_html}
            </div>
            """
            st.markdown(summary_html, unsafe_allow_html=True)

if constraints:
    with st.expander("DOMAIN CONSTRAINTS", expanded=True):
        domain_config = {
            "PROD": {"name": "Product",      "class": "card-prod"},
            "FE":   {"name": "Frontend",     "class": "card-fe"},
            "BE":   {"name": "Backend",      "class": "card-be"},
            "DS":   {"name": "Data Science", "class": "card-ds"},
            "UI":   {"name": "UI/UX",        "class": "card-ui"},
        }

        constraint_items = list(constraints.items())
        for i in range(0, len(constraint_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(constraint_items):
                    domain, data = constraint_items[i + j]

                    tech_text  = parse_markdown(data.get("text", ""))
                    biz_text   = parse_markdown(data.get("business", ""))
                    deep_dive  = parse_markdown(data.get("deep_dive", ""))
                    conf       = domain_config.get(domain, {"name": domain, "class": "card-be"})

                    deep_dive_html = (
                        f"<details class='deep-dive'><summary>Deep Dive</summary><div class='deep-content'>{deep_dive}</div></details>"
                        if deep_dive else ""
                    )

                    html_content = f"""
                    <div class='tech-card {conf['class']}'>
                        <input type='checkbox' id='toggle-{domain}' class='jargon-toggle'>
                        <div class='card-header'>
                            <div class='card-title'>{conf['name']}</div>
                            <label for='toggle-{domain}' class='jargon-label'>Translate</label>
                        </div>
                        <div class='tech-text'><b>Engineering Req:</b><br>{tech_text}</div>
                        <div class='biz-text'><b>Business Impact:</b><br>{biz_text}</div>
                        {deep_dive_html}
                    </div>
                    """
                    cols[j].markdown(html_content, unsafe_allow_html=True)

if glossary:
    with st.expander("PROJECT DICTIONARY", expanded=False):
        terms_html = ""
        for term, definition in glossary.items():
            clean_def = parse_markdown(definition).replace("In Project Naur, ", "").replace("Project Naur", "This project")
            terms_html += f"<div class='glossary-term'>{term}</div><div class='glossary-definition'>{clean_def}</div>"
        st.markdown(f"<div class='glossary-section'>{terms_html}</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
thread = sm.get_chat_history()

for msg in thread:
    clean_content = re.sub(r' \[Context: .*?\]', '', msg["content"])
    clean_content = re.sub(r' \[Governance: .*?\]', '', clean_content)

    if msg["role"] == "human":
        avatar_initials = "U"
        if "[Product" in clean_content:  avatar_initials = "PM"
        elif "[Frontend" in clean_content: avatar_initials = "FE"
        elif "[Backend" in clean_content:  avatar_initials = "BE"
        elif "[Data" in clean_content:     avatar_initials = "DS"
        elif "[UI" in clean_content:       avatar_initials = "UI"

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
        stamped_intent += f" [Context: {global_context} | Governance: {gov_phase}]"
    else:
        stamped_intent += f" [Governance: {gov_phase}]"
    sm.append_message("human", stamped_intent)
    st.rerun()
