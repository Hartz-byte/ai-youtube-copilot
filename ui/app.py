import sys
from pathlib import Path
import os

# Disable Chroma / PostHog Telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"

# Set Project Root
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
from core.controller import run_shorts, run_long_video

# Mermaid Renderer (Stable)
def render_mermaid(code: str):
    """
    Renders raw Mermaid code safely.
    DO NOT pass markdown fences.
    """

    html_code = f"""
    <div class="mermaid">
        {code}
    </div>

    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark',
            securityLevel: 'loose'
        }});
    </script>
    """

    st.components.v1.html(html_code, height=500, scrolling=True)

# Streamlit Page Config
st.set_page_config(
    page_title="AI YouTube Copilot",
    page_icon="🎬",
    layout="wide"
)

# Premium UI Styling
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: #ffffff;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #ff4b4b;
    color: white;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #ff7575;
    box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
}

.stTextInput>div>div>input {
    background-color: #262730;
    color: white;
    border-radius: 10px;
}

h1 {
    color: #ff4b4b;
}
</style>
""", unsafe_allow_html=True)

# UI Layout
st.title("🎬 AI YouTube Copilot")
st.markdown("*Your AI-powered content engineering system*")

with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.selectbox("Select Mode", ["Shorts", "Long Video"], index=0)
    level = st.selectbox("Explanation Level", ["Beginner", "Student", "Interviewer"], index=2)
    st.divider()
    st.info("System optimized for RTX 3050 (4GB VRAM). Running fully local.")

# SHORTS MODE
if mode == "Shorts":

    st.subheader("🚀 Shorts Generator")

    topic = st.text_input(
        "Enter Topic or Tool Name",
        placeholder="e.g. What is RAG?"
    )

    if st.button("Generate Script") and topic:

        with st.spinner("Generating script and diagram..."):
            result = run_shorts(topic, level)

        st.success("✅ Script Generated!")

        tab1, tab2, tab3 = st.tabs(["📜 Script", "📊 Diagram", "📑 Export Info"])

        with tab1:
            st.markdown(f"### {topic}")
            st.write(result["explanation"])

        with tab2:
            st.markdown("### 📊 Conceptual Architecture")
            render_mermaid(result["diagram"])

            with st.expander("🛠️ View Source Code"):
                st.code(result["diagram"], language="mermaid")

        with tab3:
            st.info(f"Markdown saved to: `{result['markdown']}`")
            st.info(f"Teleprompter saved to: `{result['teleprompter']}`")

# LONG VIDEO MODE
else:

    st.subheader("🎥 Long Video Walkthrough")

    repo = st.text_input(
        "GitHub Repo URL",
        placeholder="https://github.com/user/repo"
    )

    if st.button("Analyze Repository") and repo:

        with st.spinner("Cloning and analyzing repository..."):
            result = run_long_video(repo, level)

        st.success("✅ Analysis Complete!")

        t1, t2, t3 = st.tabs(["📖 Walkthrough", "📊 Architecture", "💾 Exports"])

        with t1:
            st.markdown("### Deep Walkthrough")
            st.write(result["explanation"])

        with t2:
            st.markdown("### 📊 System Architecture")
            render_mermaid(result["diagram"])

            with st.expander("🛠️ View Source Code"):
                st.code(result["diagram"], language="mermaid")

            st.info("Tip: Paste code into https://mermaid.live for high-res export.")

        with t3:
            st.markdown("### Files Generated")
            st.write(f"- **Markdown Walkthrough:** `{result['markdown']}`")
            st.write(f"- **Teleprompter Script:** `{result['teleprompter']}`")
