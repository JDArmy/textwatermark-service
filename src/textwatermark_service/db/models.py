"""Models"""
# pylint: disable=too-few-public-methods

from typing import Any

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Worker(Base):
    """Worker model"""

    __tablename__ = "workers"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    params = Column(JSON)
    use_job_id = Column(Boolean)
    text = Column(String(65535))
    created = Column(DateTime)

    jobs = relationship("Job", back_populates="worker")


class Job(Base):
    """Job model"""

    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    wm_str = Column(String(1024))
    created = Column(DateTime)

    worker = relationship("Worker", back_populates="jobs")
