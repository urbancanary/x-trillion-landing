"""
X-Trillion Minerva - AI-Powered Financial Intelligence
Landing page and showcase for the Minerva platform

This is a showcase website that demonstrates Minerva's capabilities
and directs users to the full application.
"""
import streamlit as st
from pathlib import Path
import base64
import sys

# Add src to path for demo client
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import demo client for live data
try:
    from demo_client import get_demo_response
    DEMO_AVAILABLE = True
except ImportError as e:
    DEMO_AVAILABLE = False
    print(f"Demo client not available: {e}")

# The main Minerva app is at claude_agent_new_v11
MINERVA_APP_URL = "https://minerva.x-trillion.com"

# Page config
st.set_page_config(
    page_title="Minerva | X-Trillion",
    page_icon="assets/minerva.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark, modern aesthetic
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Dark theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%);
    }

    /* Hero section - compact */
    .hero-container {
        text-align: center;
        padding: 5px 20px 5px 20px;
    }

    /* Use full page */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        margin-top: 10px;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        color: #a0a0a0;
        margin-bottom: 10px;
    }

    .tagline {
        font-size: 1rem;
        color: #888;
        font-style: italic;
    }

    /* Agent cards - centered with image inside */
    .agent-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px 10px;
        text-align: center;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 160px;
    }

    .agent-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(102, 126, 234, 0.5);
    }

    .agent-name {
        font-size: 1rem;
        font-weight: 600;
        color: #fff;
        margin: 3px 0 2px 0;
    }

    .agent-role {
        font-size: 0.65rem;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }

    .agent-desc {
        color: #aaa;
        font-size: 0.75rem;
        line-height: 1.3;
    }

    /* Section headers - compact */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        text-align: center;
        margin: 25px 0 15px 0;
    }

    .section-subheader {
        font-size: 1.1rem;
        color: #888;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Feature list */
    .feature-item {
        background: rgba(102, 126, 234, 0.1);
        border-left: 3px solid #667eea;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }

    .feature-title {
        color: #fff;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 3px;
    }

    .feature-desc {
        color: #aaa;
        font-size: 0.78rem;
    }

    /* CTA Button */
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        display: inline-block;
        text-decoration: none;
        margin: 20px 10px;
        transition: all 0.3s ease;
    }

    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #666;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 60px;
    }

    /* Chat interface */
    .chat-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Stats - compact */
    .stat-box {
        text-align: center;
        padding: 15px 10px;
    }

    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        color: #888;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

</style>
""", unsafe_allow_html=True)


def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def render_agent_card(agent, assets_dir):
    """Render agent card with centered image inside"""
    agent_img = assets_dir / agent["image"]
    img_html = ""
    if agent_img.exists():
        img_data = get_image_base64(str(agent_img))
        if img_data:
            img_html = f'<img src="data:image/png;base64,{img_data}" style="width: 45px; height: 45px; border-radius: 50%; object-fit: cover; margin-bottom: 4px;">'

    return f"""
    <div class="agent-card-mini">
        {img_html}
        <div class="agent-name">{agent['name']}</div>
        <div class="agent-role">{agent['role']}</div>
    </div>
    """


def main():
    # Get asset paths
    assets_dir = Path(__file__).parent / "assets"
    # Video served from Cloudflare R2 CDN for fast loading
    minerva_video = "https://assets.x-trillion.com/minerva-welcome.mp4"

    # Track demo response (replaces video)
    if "demo_response" not in st.session_state:
        st.session_state.demo_response = None
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None

    # Agents data
    agents = [
        {"name": "Isla", "role": "IMF Data", "image": "isla.png"},
        {"name": "Wade", "role": "World Bank", "image": "wade.png"},
        {"name": "Fred", "role": "FRED Data", "image": "fred.png"},
        {"name": "Nina", "role": "NFA Data", "image": "nina.png"},
        {"name": "Clara", "role": "Charts", "image": "clara.png"},
        {"name": "Polly", "role": "Fact-Check", "image": "polly.png"},
        {"name": "Wren", "role": "Reports", "image": "wren.png"},
        {"name": "Grace", "role": "General", "image": "grace.png"},
    ]

    # Mini agent card styling
    st.markdown("""
    <style>
        .agent-card-mini {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px 8px;
            text-align: center;
            min-height: 100px;
            margin-bottom: 8px;
        }
        .agent-card-mini:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(102, 126, 234, 0.5);
        }
        .agent-card-mini .agent-name {
            font-size: 0.8rem;
            margin: 3px 0 2px 0;
        }
        .agent-card-mini .agent-role {
            font-size: 0.6rem;
        }
        /* Video styling */
        [data-testid="stVideo"] {
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        [data-testid="stVideo"] video {
            border-radius: 12px !important;
            width: 100% !important;
            height: auto !important;
            max-height: 600px !important;
            object-fit: contain !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section - Image/Chart (left) + Title & Agents (right)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Handle pending query - fetch data with spinner in left column
        if st.session_state.get("pending_query"):
            query = st.session_state.pending_query
            st.session_state.pending_query = None
            with st.spinner("Fetching data..."):
                text, chart_html, agent_name = get_demo_response(query)
            st.session_state.demo_response = (text, chart_html, agent_name, query)
            st.rerun()

        # Show chart if we have a response, otherwise show Minerva image
        if st.session_state.demo_response:
            text, chart_html, agent_name, query = st.session_state.demo_response

            # Compact response display
            st.markdown(f"""
            <div style="background: rgba(102, 126, 234, 0.2); padding: 8px 12px; border-radius: 8px; margin-bottom: 5px;">
                <strong style="color: #667eea;">You:</strong>
                <span style="color: #fff;"> {query}</span>
            </div>
            <div style="margin-bottom: 5px;">
                <strong style="color: #888;">{agent_name}:</strong>
                <span style="color: #ccc; font-size: 0.85rem;">{text.split(chr(10))[0][:100]}...</span>
            </div>
            """, unsafe_allow_html=True)

            # Chart
            if chart_html:
                st.components.v1.html(chart_html, height=380)
        else:
            # Show Minerva video from R2 CDN
            st.video(minerva_video, autoplay=True, loop=True, muted=True)

    with col_right:
        st.markdown("""
        <div style="padding: 5px 0;">
            <h1 style="font-size: 2rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 5px 0;">MINERVA</h1>
            <p style="color: #888; font-size: 0.85rem; margin: 0 0 10px 0;">AI-Powered Financial Intelligence from X-Trillion</p>
        </div>
        """, unsafe_allow_html=True)

        # Agents grid 4x2
        for row in range(2):
            cols = st.columns(4)
            for i, col in enumerate(cols):
                agent_idx = row * 4 + i
                if agent_idx < len(agents):
                    with col:
                        st.markdown(render_agent_card(agents[agent_idx], assets_dir), unsafe_allow_html=True)

        # Spacing before chat input
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

        # Chat input under agents
        prompt = st.chat_input("Try: 'Show me US inflation' or 'What's the unemployment rate?'", key="chat_main")
        if prompt:
            if DEMO_AVAILABLE:
                st.session_state.pending_query = prompt
                st.rerun()

    # Capabilities Section
    st.markdown('<h2 style="font-size: 1.6rem; font-weight: 700; color: #fff; text-align: center; margin: 15px 0 15px 0;">What Minerva Can Do</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Natural Language Queries</div>
            <div class="feature-desc">Ask questions in plain English. "What's US inflation?" or "Show me Brazil's GDP growth from IMF."</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Multi-Source Economic Data</div>
            <div class="feature-desc">Access data from FRED (US), IMF (190+ countries), World Bank (development indicators), and Net Foreign Assets.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Dynamic Chart Generation</div>
            <div class="feature-desc">Clara creates professional visualizations - line charts, bar charts, comparisons - tailored to your query.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Political Fact-Checking</div>
            <div class="feature-desc">Polly analyzes political claims and provides fact-checked analysis with reliable sources.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Report Generation</div>
            <div class="feature-desc">Wren builds premium reports combining data, charts, and analysis into polished documents.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-item">
            <div class="feature-title">Agent Collaboration</div>
            <div class="feature-desc">Specialized agents work together - ask a complex question and the right experts collaborate to answer it.</div>
        </div>
        """, unsafe_allow_html=True)

    # Contact form dialog
    @st.dialog("Contact Us")
    def show_contact_form():
        st.markdown("We'd love to hear from you!")
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message", height=100)
        if st.button("Send Message", type="primary", use_container_width=True):
            if name and email and message:
                st.success("Thanks for reaching out! We'll be in touch soon.")
            else:
                st.warning("Please fill in all fields.")

    if "show_contact" not in st.session_state:
        st.session_state.show_contact = False

    # CTA Section - compact
    st.markdown('<h3 style="color: #fff; font-size: 1.2rem; text-align: center; margin: 10px 0 10px 0;">Ready to transform your workflow?</h3>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
    with col2:
        st.link_button("Launch Minerva", "https://minerva.x-trillion.com", type="primary", use_container_width=True)
    with col3:
        if st.button("Contact Us", use_container_width=True):
            st.session_state.show_contact = True
            st.rerun()

    if st.session_state.show_contact:
        show_contact_form()
        st.session_state.show_contact = False

    # Footer - compact
    st.markdown("""
    <div style="text-align: center; padding: 8px; color: #666; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 5px; font-size: 0.75rem;">
        <strong>X-Trillion</strong> | AI-Powered Financial Intelligence | © 2025
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
