from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

class VectorStore:
    def __init__(self, chroma_dir: str):
        self.embedding = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.store = Chroma(
            persist_directory=chroma_dir,
            embedding_function=self.embedding
        )

    def similarity_search(self, text, k=2, filter=None):
        return self.store.similarity_search(text, k=k, filter=filter)

    def add_documents(self, docs):
        self.store.add_documents(docs)
