from pydantic import BaseModel
from typing import List


class Evidence(BaseModel):
    source_id: str
    excerpt: str
    timestamp: str | None
    confidence: float


class Entity(BaseModel):
    name: str
    type: str


class Claim(BaseModel):
    subject: str
    relation: str
    object: str
    evidence: Evidence


class ExtractionResult(BaseModel):
    entities: List[Entity]
    claims: List[Claim]