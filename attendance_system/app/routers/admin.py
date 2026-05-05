from fastapi import APIRouter

router = APIRouter()

@router.get("/create")
def create_page():
    return {"message": "這是建立頁面"}