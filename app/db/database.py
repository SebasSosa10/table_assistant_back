from pathlib import Path
from urllib.parse import quote_plus
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "table_assistant")
POSTGRES_SSLMODE = os.getenv("POSTGRES_SSLMODE", "prefer")

if not POSTGRES_USER or not POSTGRES_PASSWORD:
    raise ValueError("POSTGRES_USER y POSTGRES_PASSWORD deben estar definidos en el archivo .env")

if POSTGRES_PASSWORD in {"PEGA_AQUI_LA_CLAVE_DE_SUPABASE", "[YOUR-PASSWORD]", "YOUR-PASSWORD"}:
    raise ValueError(
        "POSTGRES_PASSWORD sigue siendo un placeholder. "
        "En Supabase: Project Settings → Database → Reset database password, "
        "y pega esa clave en el archivo .env."
    )

DATABASE_URL = (
    f"postgresql+psycopg2://{quote_plus(POSTGRES_USER)}:{quote_plus(POSTGRES_PASSWORD)}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?sslmode={POSTGRES_SSLMODE}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
