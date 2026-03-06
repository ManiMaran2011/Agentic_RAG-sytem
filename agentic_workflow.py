import os
import json
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
)

class ProposalState(TypedDict):
    rfp_docs: List
    user_profile: dict
    extracted_requirements: List[str]
    matched_requirements: List[dict]
    proposal_draft: str
    gaps: List[str]
    score_explanation: str
    audit_log: List[str]


def extract_requirements(state: ProposalState):

    full_text = "\n".join([doc.page_content for doc in state["rfp_docs"]])

    prompt = f"""
Extract ONLY explicit contractor requirements.
Return valid JSON list.
No markdown.
No explanation.

RFP:
{full_text}
"""

    response = llm.invoke(prompt)

    try:
        requirements = json.loads(response.content.strip())
    except:
        requirements = [
            line.strip("- ").strip()
            for line in response.content.split("\n")
            if line.strip()
        ]

    return {
        "extracted_requirements": requirements,
        "audit_log": [f"Extracted {len(requirements)} requirements"]
    }


def match_capabilities(state: ProposalState):

    matched = []
    gaps = []

    for req in state["extracted_requirements"]:

        prompt = f"""
You are a federal compliance auditor.

Requirement:
{req}

User Profile:
{json.dumps(state["user_profile"], indent=2)}

Respond ONLY in valid JSON.
No markdown.

Format:
{{
  "status": "MET" or "GAP",
  "evidence": "Exact field supporting decision",
  "confidence": "High" or "Medium" or "Low",
  "remediation": "If GAP suggest fix else null"
}}
"""

        response = llm.invoke(prompt)

        try:
            parsed = json.loads(response.content.strip())
        except:
            parsed = {
                "status": "GAP",
                "evidence": "LLM parsing failed",
                "confidence": "Low",
                "remediation": "Manual review required"
            }

        status = str(parsed.get("status", "")).strip().upper()

        matched.append({
            "requirement": req,
            "status": status,
            "evidence": parsed.get("evidence", ""),
            "confidence": parsed.get("confidence", "Low"),
            "remediation": parsed.get("remediation", None)
        })

        if status != "MET":
            gaps.append(req)

    return {
        "matched_requirements": matched,
        "gaps": gaps,
        "audit_log": state["audit_log"] + [
            "Matched capabilities",
            f"Identified {len(gaps)} gaps"
        ]
    }


def draft_proposal(state: ProposalState):

    prompt = f"""
Draft professional federal proposal using ONLY:

User Profile:
{json.dumps(state["user_profile"], indent=2)}

Matched:
{json.dumps(state["matched_requirements"], indent=2)}

Do not fabricate.
"""

    response = llm.invoke(prompt)

    return {
        "proposal_draft": response.content,
        "audit_log": state["audit_log"] + ["Generated proposal draft"]
    }


def explain_score(state: ProposalState):

    total = len(state["matched_requirements"])
    gaps = len(state["gaps"])

    score = round(((total - gaps) / total) * 100, 2) if total > 0 else 0

    prompt = f"""
Explain briefly why compliance score is {score}%.
Total requirements: {total}
Unmet requirements: {gaps}
"""

    response = llm.invoke(prompt)

    return {
        "score_explanation": response.content,
        "audit_log": state["audit_log"] + ["Compliance score computed"]
    }


def build_agent():

    graph = StateGraph(ProposalState)

    graph.add_node("extract", extract_requirements)
    graph.add_node("match", match_capabilities)
    graph.add_node("draft", draft_proposal)
    graph.add_node("explain", explain_score)

    graph.set_entry_point("extract")

    graph.add_edge("extract", "match")
    graph.add_edge("match", "draft")
    graph.add_edge("draft", "explain")
    graph.add_edge("explain", END)

    return graph.compile()