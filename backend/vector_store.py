from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embedding_model = OllamaEmbeddings(
    model="llama3"
)

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

def store_vectors(chunks):

    vector_db.add_texts(chunks)

    vector_db.persist()