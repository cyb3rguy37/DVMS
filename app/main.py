from fastapi import FastAPI

#from app.api.routers import admin, auth
from app.core.config import settings
from app.api.routers import admin, audit, auth, visitors, visits

app = FastAPI(title=settings.app_name)

@app.get("/")
def root():
    return {"app": settings.app_name, "status": "running"}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(visitors.router)
app.include_router(audit.router)
app.include_router(visits.router)