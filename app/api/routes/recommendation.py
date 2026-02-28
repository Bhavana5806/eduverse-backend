from fastapi import APIRouter
from app.agents.adaptive_agent import generate_recommendation
from app.db.schemas import RecommendationRequest, RecommendationResponse

router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_plan(data: RecommendationRequest):

    recommendation = generate_recommendation(
        data.status,
        data.percentage
    )

    return recommendation