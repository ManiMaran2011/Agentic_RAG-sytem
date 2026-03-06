from pdf_loader import load_pdf
from rag_pipeline import chunk_documents, create_vector_store, retrieve_relevant_chunks
from proposal_generator import generate_proposal
import json

# Load RFP
docs = load_pdf("rfp.pdf")

# Chunk
chunks = chunk_documents(docs)

# Embed
vector_store = create_vector_store(chunks)

# Load user profile
with open("user_profile.json") as f:
    user_profile = json.load(f)

query = "Generate a compliant proposal response."

# Retrieve
relevant_docs = retrieve_relevant_chunks(vector_store, query)

context = "\n\n".join([doc.page_content for doc in relevant_docs])

# Generate
proposal = generate_proposal(context, user_profile)

print(proposal)