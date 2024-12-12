from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.exceptions import AppException
from config import settings

connect_args = {
    "sslmode": "require" if settings.db_ssl else "prefer",
    "application_name": settings.app_name,
}

if settings.db_connection_pool:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        pool_size=15,
        max_overflow=5,
        pool_pre_ping=True,
        connect_args=connect_args,
    )
else:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool, connect_args=connect_args
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except (DBAPIError, IntegrityError) as exc:
        db.rollback()
        raise AppException.BadRequestException(
            error_message=f"DatabaseError({exc.orig.args[0]})",
            context=f"DatabaseError({exc})",
        )
    finally:
        db.close()
