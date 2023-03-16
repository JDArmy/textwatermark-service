"""Models"""
# pylint: disable=too-few-public-methods

from typing import Any

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from .database import Base


class Worker(Base):
    """Worker model"""

    __tablename__ = "workers"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    params = Column(JSON)
    use_job_id = Column(Boolean)
    last_job_id = Column(Integer)
    text = Column(String(65535))
    created = Column(DateTime)

    jobs: Mapped["Job"] = relationship("Job", back_populates="worker")


class Job(Base):
    """Job model"""

    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), primary_key=True)
    wm_str = Column(String(1024), default="")
    created = Column(DateTime)

    worker: Mapped["Worker"] = relationship("Worker", back_populates="jobs")
