 Agentic RAG Compliance & Proposal Engine

This is an AI-powered compliance analysis and proposal generation system designed to help contractors understand government RFPs and automatically generate structured proposal drafts.

This project demonstrates an Agentic Retrieval-Augmented Generation (RAG) architecture where AI agents extract RFP requirements, evaluate contractor compliance, and generate explainable insights along with proposal drafts.

Repository: https://github.com/ManiMaran2011/Agentic_RAG-sytem

Overview

Government RFPs (Requests for Proposals) are often lengthy and complex, making it difficult for contractors to quickly identify key requirements and prepare compliant proposals.

GovPreneurs simplifies this process by using AI to:

Extract key requirements from RFP documents

Evaluate contractor compliance

Provide explainable scoring insights

Automatically generate proposal drafts

Export proposals as PDFs

Display insights through an analytics dashboard

The system acts as an AI proposal assistant, helping organizations respond to RFPs more efficiently.

Key Features
RFP Requirement Extraction

Automatically analyzes RFP documents and extracts important requirements and evaluation criteria.

Compliance Scoring

Evaluates how well a contractor meets the RFP requirements and generates transparent compliance scores with explanations.

AI Proposal Generation

Uses LLMs to generate structured proposal drafts aligned with extracted RFP requirements.

PDF Export

Generated proposals can be exported as submission-ready PDF documents.

Analytics Dashboard

Provides visual insights including:

Compliance scores

Requirement coverage

Proposal insights

Architecture

GovPreneurs uses an Agentic RAG pipeline powered by LangGraph.

Workflow:

RFP document ingestion

Requirement extraction

Context retrieval

Compliance evaluation

Proposal draft generation

Analytics visualization

PDF export

This multi-step agent workflow improves accuracy, reasoning, and explainability compared to simple prompt-based systems.

Tech Stack
Backend

FastAPI

LangGraph

OpenAI API

Frontend

React

Database

SQLite

AI Architecture

Agentic Retrieval-Augmented Generation (RAG)

System Workflow

User uploads an RFP document.

The system extracts key requirements.

Contractor information is evaluated against the requirements.

AI generates compliance scores with explanations.

A proposal draft is generated.

Users can review analytics and export the proposal as a PDF.

Installation

Clone the repository

git clone https://github.com/ManiMaran2011/Agentic_RAG-sytem.git

Navigate to the project directory

cd Agentic_RAG-sytem

Install backend dependencies

pip install -r requirements.txt

Run the backend server

uvicorn main:app --reload

Run the frontend

npm install
npm run dev
Environment Variables

Create a .env file in the root directory and add your API key.

OPENAI_API_KEY=your_api_key_here
Future Improvements

Vector database integration

Multi-agent reasoning workflows

Advanced compliance evaluation

Proposal customization templates

Multi-document RFP analysis

Integration with procurement portals

License

MIT License

Author

ManiMaran

AI developer focused on building agentic AI systems, RAG architectures, and intelligent automation tools.
