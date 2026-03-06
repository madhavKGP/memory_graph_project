from pydantic import BaseModel
from typing import List, Optional


class EmailArtifact(BaseModel):
    message_id: str
    timestamp: Optional[str]
    sender: Optional[str]
    recipients: List[str]
    subject: Optional[str]
    body: str