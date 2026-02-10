from langchain_community.vectorstores import Chroma
from config import CHROMA_DB_DIR
from rag.embedder import get_embedder

def build_vectorstore(chunks):
    embedder = get_embedder()
    return Chroma.from_texts(
        chunks,
        embedding=embedder,
        persist_directory=CHROMA_DB_DIR
    )

def query_vectorstore(query, k=5):
    embedder = get_embedder()
    db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embedder)
    docs = db.similarity_search(query, k=k)
    return "\n".join([d.page_content for d in docs])

