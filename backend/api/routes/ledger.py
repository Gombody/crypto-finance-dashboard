from fastapi import APIRouter

router = APIRouter(prefix="/ledger", tags=["ledger"])


@router.get("/health")
def ledger_health() -> dict[str, str]:
    return {"status": "ok", "module": "ledger"}