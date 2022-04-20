from fastapi import APIRouter

from apps.users.routes import router as user_router
from apps.events_config.routes import router as setting_for_users
v1_router = APIRouter(prefix='/api/v1')

v1_router.include_router(user_router)
v1_router.include_router(setting_for_users)
