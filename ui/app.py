import sys
from pathlib import Path
import os

# Set root directory
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from core.controller import run_shorts, run_long_video

st.set_page_config(
    page_title="AI YouTube Copilot",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Premium Look
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
    .css-1y4p8pa {
        padding: 2rem 5rem;
    }
    .reportview-container .main .block-container {
        max-width: 1200px;
    }
    h1 {
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 AI YouTube Copilot")
st.markdown("*Your AI-powered content engineering system*")

with st.sidebar:
    st.header("⚙️ Configuration")
    mode = st.selectbox("Select Mode", ["Shorts", "Long Video"], index=0)
    level = st.selectbox("Explanation Level", ["Beginner", "Student", "Interviewer"], index=1)
    st.divider()
    st.info("System optimized for RTX 3050. Running fully local.")

if mode == "Shorts":
    st.subheader("🚀 Shorts Generator")
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("Enter Topic or Tool Name", placeholder="e.g. What is RAG?")
    with col1:
        if st.button("Generate Script"):
            with st.spinner("Analyzing and Generating..."):
                result = run_shorts(topic, level)
                
                st.success("✅ Script Generated!")
                
                tab1, tab2 = st.tabs(["📜 Script", "📑 Export Info"])
                
                with tab1:
                    st.markdown(f"### {topic}")
                    st.write(result["explanation"])
                
                with tab2:
                    st.info(f"Markdown saved to: `{result['markdown']}`")
                    st.info(f"Teleprompter saved to: `{result['teleprompter']}`")

else:
    st.subheader("🎥 Long Video walkthrough")
    col1, col2 = st.columns([3, 1])
    with col1:
        repo = st.text_input("GitHub Repo URL", placeholder="https://github.com/user/repo")
    
    if st.button("Analyze Repository"):
        with st.spinner("Cloning and Analyzing... (This may take a minute)"):
            result = run_long_video(repo, level)
            
            st.success("✅ Analysis Complete!")
            
            t1, t2, t3 = st.tabs(["📖 Walkthrough", "📊 Architecture", "💾 Exports"])
            
            with t1:
                st.markdown("### Deep Walkthrough")
                st.write(result["explanation"])
            
            with t2:
                st.markdown("### System Architecture")
                st.code(result["diagram"], language="mermaid")
                st.info("Copy the code above into [Mermaid Live Editor](https://mermaid.live) for high-res images.")
            
            with t3:
                st.markdown("### Files Generated")
                st.write(f"- **Markdown Walkthrough:** `{result['markdown']}`")
                st.write(f"- **Teleprompter Script:** `{result['teleprompter']}`")
