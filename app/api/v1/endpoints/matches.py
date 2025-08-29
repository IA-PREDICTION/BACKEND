from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_matches_route():
    return {"message": "Route users OK"}
