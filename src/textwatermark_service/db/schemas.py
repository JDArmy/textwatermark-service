"""Table schemes"""
# pylint: disable=too-few-public-methods, missing-class-docstring
# mypy: disable-error-code=attr-defined

from datetime import datetime

from pydantic import BaseModel, Field
from textwatermark.defines import WMMode
from textwatermark.template_type import WMTemplateType
from textwatermark.version import __version__

from ..config import settings


class WMPARAMS(BaseModel):
    """Equal to params json export from TextWatermark CMD"""

    tpl_type: str = Field(default=WMTemplateType.INVISIBLE_CHARS.name)
    confusables_chars: list | dict = Field(default=[])
    confusables_chars_key: str = Field(default="")
    wm_base: int = Field(
        default=len(WMTemplateType.INVISIBLE_CHARS.value.CONFUSABLES_CHARS), gw=2, le=36
    )
    method: str = Field(default=WMTemplateType.INVISIBLE_CHARS.value.method.name)
    wm_mode: str = Field(default=WMMode.REAL_NUMBER.name)
    wm_len: int = Field(default=len(str(settings.MAX_JOB_ID)))
    wm_flag_bit: bool = Field(default=True)
    wm_loop: bool = Field(default=False)
    wm_max: str = Field(default=str(settings.MAX_JOB_ID))
    start_at: int = Field(default=1)
    version: str = Field(default=__version__)


class WorkerBase(BaseModel):
    params: WMPARAMS
    use_job_id: bool = Field(default=True)
    last_job_id: int = Field(default=0)
    text: str = Field(default="", max_length=65535)


class WorkerCreate(WorkerBase):
    created: datetime = datetime.now()


class Worker(WorkerBase):
    id: int

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    id: int
    worker_id: int
    wm_str: str = Field(default="", max_length=1024)


class JobCreate(JobBase):
    created: datetime = datetime.now()


class Job(JobBase):
    worker: list[Worker] = []

    class Config:
        orm_mode = True
