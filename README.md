# AI YouTube Copilot

AI YouTube Copilot is a local, AI-powered content engineering system designed to transform technical topics and GitHub repositories into high-quality YouTube scripts and architectural diagrams. The system is optimized for local execution on mid-range hardware (optimized for NVIDIA RTX 3050 4GB VRAM) and focuses on technical accuracy, narrative flow, and grounding to prevent hallucinations.

## Core Features

- **Shorts Generation**: Creates high-energy, fast-paced scripts limited to 150 words (approx. 60 seconds). Includes unique technical pro-tips and industry-standard gotchas.
- **Long Video Synthesis**: Analyzes entire GitHub repositories to generate a cohesive technical story. It synthesizes individual file explanations into a professional deep-dive narrative suitable for 10-minute videos.
- **Interviewer Level Depth**: Provides architectural insights, trade-offs, and scalability analysis. It includes a "Master Class Prep" section for personal high-level interview learning.
- **Hallucination Validator**: Implements a dual-pass verification system that cross-references AI-generated content against raw source code to ensure 100% technical accuracy.
- **Professional Visuals**: Generates non-linear, styled Mermaid.js diagrams for both conceptual AI terms and project architectures.
- **Structured Resource Export**: Automatically organizes scripts, markdown documentation, and teleprompter-ready text files into organized local directories.

## Architecture

The system follows a modular architecture:

- **Ingestion Layer**: Clones GitHub repositories and parses source code into structured function and class metadata.
- **RAG Layer**: Utilizes ChromaDB and Nomic-Embed-Text for local vector storage and semantic retrieval of code context.
- **Planning Layer**: A sophisticated prompt engine that applies level-specific contexts (Beginner, Student, Interviewer) and ensures script pacing.
- **Grounding Layer**: A validation module that uses a secondary LLM pass to check for unverified claims or framework biases.
- **Model Manager**: Orchestrates model switching in VRAM, clearing GPU cache between transitions to maintain system stability on limited hardware.

## Models and Hardware

The system is optimized for a fully local execution environment:

- **Primary Reasoning Model**: Llama 3 (8B Instruct) for scripts and project synthesis.
- **Code Analysis and Verification**: Mistral (7B Instruct) for high-precision technical checks.
- **Embeddings**: Nomic-Embed-Text for the vector database.
- **Hardware Optimization**: Includes manual torch CUDA cache clearing to allow model switching on 4GB VRAM GPUs.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher.
- NVIDIA GPU with CUDA support (recommended).
- Ollama installed and running.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Hartz-byte/ai-youtube-copilot.git
   cd ai-youtube-copilot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Pull required models in Ollama:
   ```bash
   ollama pull llama3:8b-instruct-q4_K_M
   ollama pull mistral:7b-instruct-q4_K_M
   ollama pull nomic-embed-text
   ```

5. Configure environment variables in a `.env` file:
   ```env
   AIYC_ROOT=D:/path/to/project
   CHROMA_DB_DIR=D:/path/to/project/vector_db
   ```

## Usage

1. Launch the application:
   ```bash
   streamlit run ui/app.py
   ```

2. Select the Mode:
   - **Shorts**: Enter a topic (e.g., "What is RAG?") or a repository URL.
   - **Long Video**: Enter a GitHub repository URL for a full project breakdown.

3. Configure the Level:
   - Set to **Interviewer** (Default) for maximum technical depth and Master Class study notes.

4. View and Export:
   - View script and live-rendered Mermaid diagrams in the UI.
   - Access saved files in the `outputs/` directory.

## Output Structure

The system organizes generated assets in a structured directory format:

- `outputs/shorts/[topic_name]/`: Contains the short script and teleprompter files.
- `outputs/long/[repo_name]/`: Contains the technical deep-dive and project walkthroughs.
- `vector_db/`: Persisted local vector storage for indexed repositories.

## Tools and Technologies

- **Frontend**: Streamlit
- **Local Inference**: Ollama
- **Vector Database**: ChromaDB
- **Framework**: LangChain
- **Analysis**: GitPython, Tree-sitter
- **Visuals**: Mermaid.js
