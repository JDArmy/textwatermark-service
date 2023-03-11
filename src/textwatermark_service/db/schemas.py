"""Table schemes"""
# pylint: disable=too-few-public-methods, missing-class-docstring

from datetime import datetime

from pydantic import BaseModel, Field
from textwatermark.defines import WMMode


class WMPARAMS(BaseModel):
    """Equal to params json export from TextWatermark CMD"""

    tpl_type: str
    confusables_chars: list | dict
    confusables_chars_key: str = Field(default="")
    wm_base: int = Field(default=2, gw=2, le=36)
    method: int
    wm_mode: int = WMMode.REAL_NUMBER
    wm_len: int
    wm_flag_bit: bool = Field(default=True)
    wm_loop: bool = Field(default=False)
    wm_max: str
    start_at: int = Field(default=0)
    version: str


class WorkerBase(BaseModel):
    params: WMPARAMS
    use_job_id: bool = Field(default=True)
    text: str = Field(max_length=65535)


class WorkerCreate(WorkerBase):
    created: datetime = datetime.now()


class Worker(WorkerBase):
    id: int

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    worker_id: int
    wm_str: str


class JobCreate(JobBase):
    created: datetime = datetime.now()


class Job(JobBase):
    id: int
    worker: list[Worker] = []

    class Config:
        orm_mode = True
