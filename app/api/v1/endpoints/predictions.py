from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_predictions_route():
    return {"message": "Route users OK"}
