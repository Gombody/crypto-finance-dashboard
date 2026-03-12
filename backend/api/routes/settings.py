from fastapi import APIRouter

from backend.config.settings import get_settings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/app")
def get_app_settings() -> dict[str, str | bool | int]:
    settings = get_settings()
    return {
        "app_name": settings.APP_NAME,
        "app_env": settings.APP_ENV,
        "app_debug": settings.APP_DEBUG,
        "display_timezone": settings.DISPLAY_TIMEZONE,
        "primary_reference_currency": settings.PRIMARY_REFERENCE_CURRENCY,
    }