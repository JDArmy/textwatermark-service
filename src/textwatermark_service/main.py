"""Main entry of service"""
# pylint: disable=invalid-name

import os
from functools import lru_cache

from fastapi import Depends, FastAPI, Form, HTTPException, Path, Query, applications
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from textwatermark.version import __version__

from . import crud
from .config import settings
from .db import models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# fixing cdn.jsdelivr.net can not be access in China problem.

app.mount(
    "/static",
    StaticFiles(directory=os.path.abspath(os.path.dirname(__file__) + "/../static")),
    name="static",
)


def swagger_monkey_patch(*args, **kwargs):
    """patch swagger"""
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch

# fix end.

# Dependency


def get_db():
    """Get db instance"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache(maxsize=2)
def check_authorize_key(authorize_key):
    """check authorize key"""
    if settings.AUTHORIZE_KEY and str(authorize_key) != str(settings.AUTHORIZE_KEY):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized. Please set the value of authorize_key "
            + "you set in docker-compose.yml",
        )


@app.post("/worker/create")
def create_worker(
    worker: schemas.WorkerCreate,
    authorize_key: str = Query(default=None),
    db: Session = Depends(get_db),
):
    """Insert worker params to db and get worker id."""
    check_authorize_key(authorize_key)

    if not worker.text:
        raise HTTPException(status_code=400, detail="text is required for watermark")

    crud.check_params(worker.params, worker.text, worker.use_job_id)

    db_worker = crud.create_worker(db=db, worker=worker)
    return {"worker_id": db_worker.id}


@app.post("/worker/{worker_id}/do_job")
def do_job_as_worker(
    wm_str: str = Form(max_length=1024, default=""),
    worker_id: int = Path(title="The ID of the worker to get", ge=1),
    authorize_key: str = Query(default=None),
    db: Session = Depends(get_db),
):
    """Do text watermark with watermark string"""
    check_authorize_key(authorize_key)

    db_worker = crud.get_worker(worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    last_job_id = crud.get_last_job_id(worker_id)
    job = schemas.JobCreate(id=last_job_id, worker_id=worker_id, wm_str=wm_str)
    db_job = crud.create_job(db=db, job=job)

    return crud.insert_watermark(job=db_job, worker=db_worker)


@app.get("/worker/{worker_id}")
def get_worker_info(
    worker_id: int = Path(title="The ID of the worker to get", ge=1),
    authorize_key: str = Query(default=None),
):
    """Get worker info from worker id"""
    check_authorize_key(authorize_key)

    db_worker = crud.get_worker(worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    return db_worker


@app.post("/worker/{worker_id}/job/{job_id}/redo")
def redo_job(
    worker_id: int = Path(title="The ID of the worker to get", ge=1),
    job_id: int = Path(title="The ID of the job to get", ge=1),
    authorize_key: str = Query(default=None),
    db: Session = Depends(get_db),
):
    """Redo the job.

    Sometimes you may want to reconfirm that the watermark
    information you retrieved is correct"""
    check_authorize_key(authorize_key)

    db_job = crud.get_job(db=db, worker_id=worker_id, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return crud.insert_watermark(
        job=db_job, worker=db_job.worker, dont_check_version=True
    )


@app.get("/worker/{worker_id}/job/{job_id}")
def get_job_info(
    worker_id: int = Path(title="The ID of the worker to get", ge=1),
    job_id: int = Path(title="The ID of the job to get", ge=1),
    authorize_key: str = Query(default=None),
    db: Session = Depends(get_db),
):
    """Get the job information"""
    check_authorize_key(authorize_key)

    db_job = crud.get_job(db=db, worker_id=worker_id, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job
