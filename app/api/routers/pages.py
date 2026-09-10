from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request}
    )

@router.get("/register-visitor", response_class=HTMLResponse)
def register_visitor_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register_visitor.html",
        context={}
    )

@router.get("/search-visitor", response_class=HTMLResponse)
def search_visitor_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="search_visitor.html",
        context={}
    )

@router.get("/active-visitors", response_class=HTMLResponse)
def active_visitors_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="active_visitors.html",
        context={}
    )

@router.get("/checkout-visitor", response_class=HTMLResponse)
def checkout_visitor_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="checkout_visitor.html",
        context={}
    )

@router.get("/reports", response_class=HTMLResponse)
def reports_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={}
    )

@router.get("/audit-verify", response_class=HTMLResponse)
def audit_verify_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="audit.html",
        context={}
    )

@router.get("/retention", response_class=HTMLResponse)
def retention_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="retention.html",
        context={}
    )