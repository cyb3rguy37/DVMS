from fastapi import FastAPI

#from app.api.routers import admin, auth
from app.core.config import settings
from app.api.routers import admin, audit, auth, pages, reports, retention, visitors, visits
from fastapi.staticfiles import StaticFiles

app = FastAPI(title=settings.app_name)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

@app.get("/")
def root():
    return {"app": settings.app_name, "status": "running"}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(visitors.router)
app.include_router(audit.router)
app.include_router(visits.router)
app.include_router(reports.router)
app.include_router(retention.router)
app.include_router(pages.router)