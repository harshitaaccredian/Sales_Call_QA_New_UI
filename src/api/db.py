"""
Database setup — SQLAlchemy 2.0 with Supabase / PostgreSQL support and Alembic migrations.

Connects to Supabase via DATABASE_URL from .env.
Falls back to local SQLite if DATABASE_URL is not set.

Call init_db() once at app startup to run Alembic migrations to head.
Use get_db() as a FastAPI dependency to obtain a per-request Session.
Use new_session() for background tasks to manage session lifecycles independently.
"""

import logging
import os
import re
import urllib.parse
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

logger = logging.getLogger(__name__)

# Resolve project root from this file's location (src/api/db.py → ../../)
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_PROJECT_ROOT / ".env")

_DB_DIR = _PROJECT_ROOT / "db"
_DB_PATH = _DB_DIR / "call_quality.db"


def sanitize_database_url(url: str | None) -> str:
    """
    Sanitize database URL:
    - Normalizes postgres:// to postgresql://
    - Removes template brackets e.g. [my-password]
    - URL-encodes special characters in credentials (e.g. @ or $)
    - Ensures sslmode=require for postgresql connections if missing
    """
    if not url:
        return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    # Match scheme://user:password@host...
    pattern = r"^(?P<prefix>[a-zA-Z0-9_+]+://)(?P<user>[^:]+):(?P<raw_pw>.+)@(?P<suffix>[^@]+)$"
    m = re.match(pattern, url)
    if m:
        prefix = m.group("prefix")
        user = m.group("user")
        pw = m.group("raw_pw")
        suffix = m.group("suffix")
        # Remove brackets if user wrote [my-password]
        if pw.startswith("[") and pw.endswith("]"):
            pw = pw[1:-1]
        encoded_pw = urllib.parse.quote(urllib.parse.unquote(pw), safe="")
        url = f"{prefix}{user}:{encoded_pw}@{suffix}"

    if url.startswith("postgresql://") and "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"

    return url


def get_database_url() -> str:
    """Return the active database connection URL from os.environ, st.secrets, or fallback to local SQLite."""
    raw_url = os.environ.get("DATABASE_URL")
    if not raw_url:
        try:
            import streamlit as st
            raw_url = st.secrets.get("DATABASE_URL")
        except Exception:
            pass

    if raw_url and str(raw_url).strip():
        return sanitize_database_url(str(raw_url).strip())

    _DB_DIR.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{_DB_PATH}"


DATABASE_URL = get_database_url()

# Configure engine based on database dialect
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,    # Test connections before using them; handles Supabase pooler disconnects
        pool_recycle=300,      # Recycle connections after 5 minutes
        pool_size=10,
        max_overflow=20,
        echo=False,
    )
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def run_migrations() -> None:
    """Run Alembic migrations programmatically up to head."""
    from alembic import command
    from alembic.config import Config

    ini_path = _PROJECT_ROOT / "alembic.ini"
    alembic_dir = _PROJECT_ROOT / "alembic"

    if not ini_path.exists():
        logger.warning(f"Alembic config not found at {ini_path}. Skipping migrations.")
        return

    alembic_cfg = Config(str(ini_path))
    alembic_cfg.set_main_option("script_location", str(alembic_dir))
    alembic_cfg.set_main_option("sqlalchemy.url", get_database_url().replace("%", "%%"))
    command.upgrade(alembic_cfg, "head")


def init_db() -> None:
    """Initialize database tables via Alembic migrations."""
    # Ensure models are imported
    from src.api.models import jobs  # noqa: F401

    try:
        run_migrations()
        logger.info("Database migrations applied successfully via Alembic.")
    except Exception as exc:
        logger.error(
            f"Failed to apply Alembic migrations: {exc}. Falling back to create_all() if needed.",
            exc_info=True,
        )
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Fallback Base.metadata.create_all() executed.")
        except Exception as fallback_exc:
            logger.error(f"Fallback create_all failed: {fallback_exc}", exc_info=True)


def get_db():
    """
    FastAPI dependency that yields a SQLAlchemy Session and closes it after
    the request, even if an exception is raised.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def new_session() -> Session:
    """
    Create a standalone Session for use outside the request/response cycle
    (e.g. inside background tasks / Streamlit). Caller is responsible for closing.
    """
    return SessionLocal()