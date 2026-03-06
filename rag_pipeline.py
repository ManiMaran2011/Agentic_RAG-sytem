# rag_pipeline.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from typing import List, Tuple
import re


# -----------------------------------
# 1️⃣ Intelligent Requirement Tagging
# -----------------------------------

def tag_requirement_type(text: str) -> str:
    """
    Tags whether chunk contains mandatory language.
    """
    mandatory_keywords = ["shall", "must", "required", "will comply"]
    for keyword in mandatory_keywords:
        if keyword.lower() in text.lower():
            return "mandatory"
    return "general"


# -----------------------------------
# 2️⃣ Chunking with Metadata Enrichment
# -----------------------------------

def chunk_documents(documents: List[Document]) -> List[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        text = chunk.page_content
        chunk.metadata["requirement_type"] = tag_requirement_type(text)
        chunk.metadata["page"] = chunk.metadata.get("page", "unknown")

    return chunks


# -----------------------------------
# 3️⃣ Vector Store Creation
# -----------------------------------

def create_vector_store(chunks: List[Document]):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# -----------------------------------
# 4️⃣ Hybrid Retrieval
# -----------------------------------

def retrieve_relevant_chunks(
    vector_store,
    query: str,
    k: int = 5
) -> Tuple[List[Document], float]:

    # Semantic retrieval
    docs = vector_store.similarity_search_with_score(query, k=k)

    retrieved_docs = []
    scores = []

    for doc, score in docs:
        # Boost mandatory sections
        if doc.metadata.get("requirement_type") == "mandatory":
            score *= 0.85  # reduce score (FAISS lower = better)

        retrieved_docs.append(doc)
        scores.append(score)

    # Compute confidence score
    avg_score = sum(scores) / len(scores) if scores else 1.0
    confidence = round(1 - avg_score, 3)

    return retrieved_docs, confidence


# -----------------------------------
# 5️⃣ Structured Context Formatter
# -----------------------------------

def format_context(docs: List[Document]) -> str:

    formatted_chunks = []

    for i, doc in enumerate(docs, start=1):
        page = doc.metadata.get("page", "unknown")
        req_type = doc.metadata.get("requirement_type", "general")

        formatted_chunks.append(
            f"""
[RFP Section {i}]
Page: {page}
Requirement Type: {req_type}
Content:
{doc.page_content}
"""
        )

    return "\n\n".join(formatted_chunks)


# -----------------------------------
# 6️⃣ End-to-End RAG Builder
# -----------------------------------

def build_rag_context(documents: List[Document], query: str):

    chunks = chunk_documents(documents)
    vector_store = create_vector_store(chunks)
    retrieved_docs, confidence = retrieve_relevant_chunks(vector_store, query)
    context = format_context(retrieved_docs)

    return context, confidence