from pydantic import BaseModel
from typing import Dict, List


class ProposalRequest(BaseModel):
    user_profile: Dict


class ProposalResponse(BaseModel):
    proposal_id: str
    draft: str
    gaps: List[str]
    status: str