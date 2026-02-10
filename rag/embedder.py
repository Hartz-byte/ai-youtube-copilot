from langchain_community.embeddings import OllamaEmbeddings
from config import EMBED_MODEL

def get_embedder():
    return OllamaEmbeddings(model=EMBED_MODEL)
