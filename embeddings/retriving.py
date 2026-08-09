from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma


# Read the text file
with open("job_listings.txt", "r", encoding="utf-8") as f:
    text = f.read()


# Convert it into a LangChain Document
documents = [
    Document(
        page_content=text,
        metadata={"source": "job_listings.txt"}
    )
]


# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=10
)

chunks = text_splitter.split_documents(documents)


# Local Ollama embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Chroma vector database
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings
)


# Retriever
retriever = db.as_retriever(
    search_kwargs={"k": 4}
)


query = input("Enter the query: ")

docs = retriever.invoke(query)

for i, doc in enumerate(docs, start=1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)