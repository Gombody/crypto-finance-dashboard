from fastapi import APIRouter

router = APIRouter(prefix="/exchanges", tags=["exchanges"])


@router.get("/health")
def exchanges_health() -> dict[str, str]:
    return {"status": "ok", "module": "exchanges"}