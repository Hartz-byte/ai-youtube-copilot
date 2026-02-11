from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["content"]):
            chunks.append({
                "text": chunk,
                "source": doc["path"]
            })

    return chunks
