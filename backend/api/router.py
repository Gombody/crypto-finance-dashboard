from fastapi import APIRouter

from backend.api.routes.alerts import router as alerts_router
from backend.api.routes.exchanges import router as exchanges_router
from backend.api.routes.ledger import router as ledger_router
from backend.api.routes.reports import router as reports_router
from backend.api.routes.settings import router as settings_router
from backend.api.routes.wallets import router as wallets_router

api_router = APIRouter()
api_router.include_router(exchanges_router)
api_router.include_router(wallets_router)
api_router.include_router(ledger_router)
api_router.include_router(reports_router)
api_router.include_router(alerts_router)
api_router.include_router(settings_router)