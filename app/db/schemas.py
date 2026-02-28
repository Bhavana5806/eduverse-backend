from pydantic import BaseModel

class PerformanceCreate(BaseModel):
    student_name: str
    subject: str
    topic: str
    score: float
    max_score: float


class WeaknessResponse(BaseModel):
    student_name: str
    subject: str
    topic: str
    percentage: float
    status: str


class RecommendationRequest(BaseModel):
    status: str
    percentage: float


class RecommendationResponse(BaseModel):
    recommended_level: str
    strategy: str
    target_score_percentage: float