"""CRUD methods"""
# pylint: disable=invalid-name,too-many-function-args

from datetime import datetime
from functools import lru_cache

from fastapi import HTTPException
from sqlalchemy.orm import Session
from textwatermark import TextWatermark

from .db import models, schemas
from .db.database import SessionLocal


@lru_cache(maxsize=128)
def get_worker(worker_id: int):
    """Get worker from db"""
    db = SessionLocal()
    try:
        # yield db
        return db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    finally:
        db.close()


def get_job(db: Session, job_id: int):
    """Get job and the related worker from db"""
    db_job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if db_job:
        db_job.worker = get_worker(db_job.worker_id)
    return db_job


def create_worker(db: Session, worker: schemas.WorkerCreate):
    """insert params to worker"""
    worker.created = datetime.now()
    db_worker = models.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker


def create_job(db: Session, job: schemas.JobCreate):
    """insert wm_str to job"""
    job.created = datetime.now()
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def insert_watermark(
    job: schemas.Job, worker: schemas.Worker, dont_check_version: bool = False
):
    """call TextWatermark for insert text watermark."""
    wm_str = job.wm_str
    if worker.use_job_id:
        wm_str = str(job.id)

    try:
        wm_init = TextWatermark.init_from_params(
            worker.params, worker.text, dont_check_version
        )
        wm_text = wm_init.insert_watermark(wm_str)
    except ValueError as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

    return {
        "use_job_id": worker.use_job_id,
        "job_id": job.id,
        "wm_str": job.wm_str,
        "wm_text": wm_text,
    }
