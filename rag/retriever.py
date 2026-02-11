# rag/retriever.py

import os
from typing import List, Dict
from langchain_community.vectorstores import Chroma
from rag.embedder import get_embedder
import chromadb
from chromadb.config import Settings

# Disable telemetry BEFORE anything
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["POSTHOG_DISABLED"] = "1"
os.environ["CHROMA_ANONYMIZED_TELEMETRY"] = "False"


def build_vectorstore(chunks: List[Dict], repo_id: str):
    persist_dir = os.path.join("vector_db", repo_id)
    os.makedirs(persist_dir, exist_ok=True)

    embedder = get_embedder()

    # If already exists, load instead of rebuilding
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedder,
            collection_name=repo_id
        )

    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c.get("source", "unknown")} for c in chunks]

    db = Chroma.from_texts(
        texts=texts,
        embedding=embedder,
        metadatas=metadatas,
        persist_directory=persist_dir,
        collection_name=repo_id
    )

    db.persist()
    return db


def query_vectorstore(query: str, repo_id: str, k: int = 5) -> str:
    persist_dir = os.path.join("vector_db", repo_id)

    if not os.path.exists(persist_dir):
        return ""

    embedder = get_embedder()

    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedder,
        collection_name=repo_id
    )

    docs = db.similarity_search(query, k=k)

    return "\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
        for d in docs
    )
