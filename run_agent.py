from agentic_workflow import build_agent
from pdf_loader import load_pdf
import json

# Load RFP
rfp_docs = load_pdf("rfp.pdf")

# Load user profile
with open("user_profile.json") as f:
    user_profile = json.load(f)

# Build agent
agent = build_agent()

# Run agent
result = agent.invoke({
    "rfp_docs": rfp_docs,
    "user_profile": user_profile,
    "extracted_requirements": [],
    "matched_requirements": [],
    "draft": "",
    "gaps": []
})

print("FINAL DRAFT:\n", result["draft"])
print("\nGAPS:\n", result["gaps"])