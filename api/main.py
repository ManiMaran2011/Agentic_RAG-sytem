import shutil
import os
import json
import sqlite3
import asyncio
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sse_starlette.sse import EventSourceResponse

from agentic_workflow import build_agent
from api.pdf_generator import generate_pdf
from api.scoring import weighted_score
from pdf_loader import load_pdf


# -----------------------
# APP INIT
# -----------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_agent()
DB = "proposals.db"


# -----------------------
# DB INIT
# -----------------------

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id TEXT PRIMARY KEY,
            draft TEXT,
            score REAL,
            risk TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -----------------------
# GENERATE PROPOSAL
# -----------------------

@app.post("/generate-proposal")
async def generate_proposal(
    file: UploadFile = File(...),
    user_profile: str = File(...)
):

    proposal_id = str(uuid4())

    # Save uploaded PDF
    temp_path = f"temp_{proposal_id}.pdf"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rfp_docs = load_pdf(temp_path)
    profile_json = json.loads(user_profile)

    # Run Agent Workflow
    result = agent.invoke({
        "rfp_docs": rfp_docs,
        "user_profile": profile_json,
        "extracted_requirements": [],
        "matched_requirements": [],
        "proposal_draft": "",
        "gaps": [],
        "score_explanation": "",
        "audit_log": []
    })

    os.remove(temp_path)

    # -----------------------
    # WEIGHTED SCORING
    # -----------------------

    score = weighted_score(result["matched_requirements"])

    # Deterministic Risk Level
    if score >= 85:
        risk = "Low"
    elif score >= 60:
        risk = "Medium"
    else:
        risk = "High"

    # Save to DB
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO proposals VALUES (?, ?, ?, ?)",
        (proposal_id, result["proposal_draft"], score, risk)
    )
    conn.commit()
    conn.close()

    return {
        "proposal_id": proposal_id,
        "draft": result["proposal_draft"],
        "matched_requirements": result["matched_requirements"],
        "gaps": result["gaps"],
        "compliance_score": score,
        "risk_level": risk,
        "score_explanation": result.get("score_explanation", ""),
        "audit_log": result.get("audit_log", []),
        "reasoning_steps": [
            f"Total requirements: {len(result['matched_requirements'])}",
            f"Gaps identified: {len(result['gaps'])}",
            f"Compliance Score: {score}%",
            f"Risk Level: {risk}"
        ]
    }


# -----------------------
# STREAMING UX (SSE)
# -----------------------

@app.get("/generate-stream")
async def generate_stream():

    async def event_generator():

        steps = [
            "Extracting requirements...",
            "Matching compliance...",
            "Drafting proposal...",
            "Computing compliance score...",
            "Finalizing output..."
        ]

        for step in steps:
            yield {
                "event": "status",
                "data": step
            }
            await asyncio.sleep(1.2)

        yield {
            "event": "complete",
            "data": "done"
        }

    return EventSourceResponse(event_generator())


# -----------------------
# DOWNLOAD PDF
# -----------------------

@app.get("/download-proposal/{proposal_id}")
def download_proposal(proposal_id: str):

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT draft, score, risk FROM proposals WHERE id=?",
        (proposal_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Proposal not found")

    file_path = f"{proposal_id}.pdf"
    generate_pdf(file_path, row[0], row[1], row[2])

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="proposal.pdf"
    )


# -----------------------
# BENCHMARKING
# -----------------------

@app.get("/benchmark")
def benchmark():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT id, score, risk FROM proposals")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "proposal_id": r[0],
            "score": r[1],
            "risk": r[2]
        }
        for r in rows
    ]