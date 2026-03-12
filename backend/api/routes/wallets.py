from fastapi import APIRouter

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.get("/health")
def wallets_health() -> dict[str, str]:
    return {"status": "ok", "module": "wallets"}