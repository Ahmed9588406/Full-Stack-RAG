from langchain_qdrant import Qdrant
from langchain_ollama import OllamaEmbeddings  # Use Ollama embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from qdrant_client import QdrantClient, models
from decouple import config

# Ollama settings
OLLAMA_EMBEDDING_MODEL = "nomic-embed-text"


qdrant_api_key = config("QDRANT_API_KEY")
qdrant_url = config("QDRANT_URL")
collection_name = "Websites"
client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key
)


ollama_embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL)
vector_Store = Qdrant(client=client, collection_name=collection_name,embeddings=ollama_embeddings)

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len
)
def create_collection(collection_name):
    # Check if collection exists
    collections = client.get_collections().collections
    exists = any(collection.name == collection_name for collection in collections)
    
    if not exists:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
        )
        print(f"Collection {collection_name} created successfully")
    else:
        print(f"Collection {collection_name} already exists")


def upload_website_to_collection(url:str):
    loader = WebBaseLoader(url)
    docs = loader.load_and_split(text_spliter)
    for doc in docs:
        doc.metadata = {"source_url":url}
    vector_Store.add_documents(docs)
    return f"Successfully uploaded {len(docs)} documents to collection {collection_name} from {url}"


#create_collection(collection_name)
#upload_website_to_collection("https://hamel.dev/blog/posts/evals/")