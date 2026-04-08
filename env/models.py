from pydantic import BaseModel
from typing import List, Optional

class Ticket(BaseModel):
    id: str
    text: str
    category: str
    priority: str
    resolved: bool = False

class Observation(BaseModel):
    current_ticket: Ticket
    history: List[str]

class Action(BaseModel):
    action_type: str
    content: Optional[str] = None

class Reward(BaseModel):
    score: float
    feedback: str