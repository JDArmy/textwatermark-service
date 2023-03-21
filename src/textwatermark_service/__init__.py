"""TextWatermark Service"""
__version__ = "0.2.2"

from . import log
from .config import settings
from .main import app

if settings.LOGENABLED:
    log.init_log()
