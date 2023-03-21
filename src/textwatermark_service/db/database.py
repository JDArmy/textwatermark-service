"""DB connection"""
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

if settings.DEBUG:
    # sqlite
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.SQLITE_PATH}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # postgres
    postgres_host = settings.POSTGRES_HOST
    postgres_port = settings.POSTGRES_PORT
    postgres_db = settings.POSTGRES_DB
    postgres_user = settings.POSTGRES_USER
    postgres_password = settings.POSTGRES_PASSWORD

    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{postgres_user}:{postgres_password}"
        + f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )

    # print("*****", "DB Connect String", SQLALCHEMY_DATABASE_URL)

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=True, bind=engine)
Base: Any = declarative_base()
