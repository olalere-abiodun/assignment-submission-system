from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Use the same templates directory path
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/lecturer/index.html", response_class=HTMLResponse)
async def serve_lecturer_dashboard(request: Request):
    return templates.TemplateResponse("lecturer/index.html", {"request": request})

@router.get("/student/index.html", response_class=HTMLResponse)
async def serve_student_dashboard(request: Request):
    return templates.TemplateResponse("student/index.html", {"request": request})

@router.get("/student/courses.html", response_class=HTMLResponse)
def get_courses(request: Request):
    return templates.TemplateResponse("student/courses.html", {"request": request})

@router.get("/student/assignments.html", response_class=HTMLResponse)
def get_assignments(request: Request):
    return templates.TemplateResponse("student/assignments.html", {"request": request})

@router.get("/student/submission.html", response_class=HTMLResponse)
def get_submission(request: Request):
    return templates.TemplateResponse("student/submission.html", {"request": request})

@router.get("/student/profile.html", response_class=HTMLResponse)
def get_profile(request: Request):
    return templates.TemplateResponse("student/profile.html", {"request": request})
