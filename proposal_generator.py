from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import json


def generate_proposal(context, user_profile, confidence_score):

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )

    system_prompt = """
You are an expert Federal Government Proposal Writer.

STRICT RULES:
- Use ONLY the provided RFP context.
- Use ONLY verified user profile data.
- Do NOT fabricate certifications, contracts, or experience.
- If required information is missing, explicitly state:
  "Insufficient user data to fully address this requirement."
- Cite RFP Section numbers when responding.
- Maintain professional, government-compliant tone.
- Avoid marketing language.
- Structure response formally.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"""
RFP CONTEXT:
{context}

USER PROFILE:
{json.dumps(user_profile, indent=2)}

RETRIEVAL CONFIDENCE SCORE:
{confidence_score}

Generate the following structured proposal:

1. Executive Summary
2. Technical Approach (map to RFP requirements explicitly)
3. Compliance Mapping Table
4. Past Performance Alignment
5. Identified Gaps (if any)

Ensure every requirement addressed references the relevant RFP Section.
""")
    ])

    chain = prompt | llm
    response = chain.invoke({})

    return response.content