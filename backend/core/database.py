from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core import config

# Connect args specific to SQLite connection pool
connect_args = {}
if config.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Central SQLAlchemy database engine pool
engine = create_engine(
    config.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency yielding a clean database session per request.
    Ensures connection is returned to pool after request processing.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initializes database tables on application startup.
    """
    from backend.models import db_models  # noqa: F401
    Base.metadata.create_all(bind=engine)
