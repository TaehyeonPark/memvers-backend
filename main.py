from fastapi import FastAPI, Depends, HTTPException, status, Request, Response, Form, Cookie, Header
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi_sessions.backends.implementations import InMemoryBackend

from sqlalchemy.orm import Session

from uvicorn import run

import uuid
from json import loads, dumps
from typing import Optional, List, Dict, Any

import models, schema, crud
import ldap
from inmemorydb import Redi
from database import SessionLocal, engine, get_db
from util import *
from session import *
from error_template import error_template
import router

app = FastAPI()
redi = router.redi
app.include_router(router.router)

@app.middleware("http")
async def session_managing_middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/login":
        return response
    if not IsUUIDValid(request, redi) and request.url.path != "/login":
        return RedirectResponse(url="/login", status_code=302)
    return response

@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return HTMLResponse(content=error_template(error_code=404, desc="Not Found"), status_code=404)

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/login", status_code=302)

@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc: Exception):
    return HTMLResponse(content=error_template(error_code=405, desc="Method Not Allowed"), status_code=405)

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return HTMLResponse(content=error_template(error_code=500, desc="Internal Server Error"), status_code=500)

@app.exception_handler(422)
async def unprocessable_entity_handler(request: Request, exc: Exception):
    return HTMLResponse(content=error_template(error_code=422, desc="Unprocessable Entity"), status_code=422)
if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)