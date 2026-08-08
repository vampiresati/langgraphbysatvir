
from typing import List, TypedDict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import StateGraph, START, END


# ---------------------------------------------------
# Current Affairs News Sources
# ---------------------------------------------------

news_urls = [
    # "https://www.bbc.com/news",
    # "https://www.cnn.com/world",
    # "https://www.nytimes.com/section/world",
    # "https://www.reuters.com/world/",
    # "https://www.aljazeera.com/news/",
    "https://www.thehindu.com/"
]


# ---------------------------------------------------
# Load Current Affairs Documents
# ---------------------------------------------------

docs = []

for url in news_urls:
    print(f"Loading: {url}")

    try:
        loaded_docs = WebBaseLoader(url).load()
        docs.extend(loaded_docs)

    except Exception as e:
        print(f"Failed to load {url}: {e}")


print(f"\nTotal documents loaded: {len(docs)}")


# ---------------------------------------------------
# Split Documents
# ---------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
)

doc_splits = text_splitter.split_documents(docs)

print(f"Total chunks created: {len(doc_splits)}")


# ---------------------------------------------------
# Hugging Face Embeddings
# ---------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------------------
# Chroma Vector Store
# ---------------------------------------------------

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="current-affairs-news",
    embedding=embeddings,
)


# ---------------------------------------------------
# Retriever
# ---------------------------------------------------

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5
    }
)


# ---------------------------------------------------
# Local Qwen Model Through Ollama
# ---------------------------------------------------

model = ChatOllama(
    model="qwen3:4b",
    temperature=0,
)


# ---------------------------------------------------
# Prompt
# ---------------------------------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are a news analyst.

Use only the retrieved news articles below to answer the user's question.

Provide a concise and clear current-affairs summary.

If the retrieved information does not contain enough information,
say that the available articles do not provide enough information.

Question:
{question}

News Articles:
{context}

Summary:
"""
)


# ---------------------------------------------------
# RAG Chain
# ---------------------------------------------------

current_affairs_chain = (
    prompt
    | model
    | StrOutputParser()
)


# ---------------------------------------------------
# LangGraph State
# ---------------------------------------------------

class CurrentAffairsGraphState(TypedDict):
    question: str
    retrieved_news: List
    generation: str


# ---------------------------------------------------
# Node 1: Retrieve Documents
# ---------------------------------------------------

def retrieve_current_affairs(state: CurrentAffairsGraphState):

    print("\n--- RETRIEVE CURRENT AFFAIRS ---")

    question = state["question"]

    retrieved_news = retriever.invoke(question)

    print(f"Retrieved documents: {len(retrieved_news)}")

    return {
        "question": question,
        "retrieved_news": retrieved_news,
    }


# ---------------------------------------------------
# Node 2: Generate Summary
# ---------------------------------------------------

def generate_current_affairs_summary(
    state: CurrentAffairsGraphState
):

    print("\n--- GENERATE CURRENT AFFAIRS SUMMARY ---")

    question = state["question"]

    # IMPORTANT:
    # Use documents retrieved by previous node.
    # Do NOT call retriever.invoke() again.
    retrieved_news = state["retrieved_news"]

    context = "\n\n".join(
        [
            doc.page_content
            for doc in retrieved_news
        ]
    )

    generation = current_affairs_chain.invoke(
        {
            "question": question,
            "context": context,
        }
    )

    return {
        "question": question,
        "retrieved_news": retrieved_news,
        "generation": generation,
    }


# ---------------------------------------------------
# Build LangGraph Workflow
# ---------------------------------------------------

def create_current_affairs_workflow():

    workflow = StateGraph(CurrentAffairsGraphState)

    workflow.add_node(
        "retrieve_current_affairs",
        retrieve_current_affairs,
    )

    workflow.add_node(
        "generate_current_affairs_summary",
        generate_current_affairs_summary,
    )

    workflow.add_edge(
        START,
        "retrieve_current_affairs",
    )

    workflow.add_edge(
        "retrieve_current_affairs",
        "generate_current_affairs_summary",
    )

    workflow.add_edge(
        "generate_current_affairs_summary",
        END,
    )

    return workflow.compile()


# ---------------------------------------------------
# Compile Graph
# ---------------------------------------------------

current_affairs_graph = create_current_affairs_workflow()


# ---------------------------------------------------
# Run
# ---------------------------------------------------

if __name__ == "__main__":

    inputs = {
        "question": "What about Jharkhand protests?"
    }

    response = current_affairs_graph.invoke(inputs)

    print("\n--------------------------------")
    print("CURRENT AFFAIRS SUMMARY")
    print("--------------------------------\n")

    print(response["generation"])
