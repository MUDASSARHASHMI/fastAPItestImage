from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.api.v1.api import router
from app.core.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
add_pagination(app)
app.include_router(router)