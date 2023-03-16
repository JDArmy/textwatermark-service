"""CRUD methods"""
# pylint: disable=invalid-name,too-many-function-args,pointless-statement

from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from textwatermark import TextWatermark
from textwatermark.version import __version__

from textwatermark_service.db.database import SessionLocal

from .db import models, schemas


def get_worker_last_job_id(db: Session, worker_id: int):
    """Get last job id from db"""
    db.commit()
    db_worker = db.query(models.Worker).with_for_update().filter(
        models.Worker.id == worker_id).first()
    if not db_worker:
        return 0

    db_worker.last_job_id += 1
    db.commit()
    db.refresh(db_worker)
    return db_worker


def get_worker(db: Session, worker_id: int):
    """Get worker from db"""
    db_worker = db.query(models.Worker).filter(
        models.Worker.id == worker_id).first()
    return db_worker


def get_job(db: Session, worker_id: int, job_id: int):
    """Get job and the related worker from db"""
    db_job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id and models.Job.worker_id == worker_id)
        .first()
    )
    if db_job:
        # get worker from db automatically by relationship
        db_job.worker
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
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

    return {
        "worker_id": worker.id,
        "job_id": job.id,
        "use_job_id": worker.use_job_id,
        "wm_str": job.wm_str,
        "wm_text": wm_text,
    }


def check_params(
    params: schemas.WMPARAMS,
    text: str,
    use_job_id: bool = True,
):
    """check if params invalid"""
    if params.version != __version__:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid version: {params.version}, " f"expected {__version__}",
        )

    if use_job_id:
        params.wm_max = "999999"

    enough = False
    try:
        enough = TextWatermark.check_if_enough_space(params.json(), text)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

    if not enough:
        raise HTTPException(
            status_code=400, detail="Not enough space for watermark")
