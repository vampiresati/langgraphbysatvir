from langchain_ollama import OllamaEmbeddings
import numpy as np

# Local Ollama embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

text1 = input("Enter text 1: ")
text2 = input("Enter text 2: ")

# Generate embeddings
response1 = embeddings.embed_query(text1)
response2 = embeddings.embed_query(text2)

# Cosine similarity
similarity_score = np.dot(response1, response2) / (
    np.linalg.norm(response1) * np.linalg.norm(response2)
)

print("Similarity:", similarity_score)
print("Similarity percentage:", similarity_score * 100, "%")