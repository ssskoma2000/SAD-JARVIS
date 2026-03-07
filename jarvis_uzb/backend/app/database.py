from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ma'lumotlar bazasi uchun URL (SQLite ishlatamiz)
SQLALCHEMY_DATABASE_URL = "sqlite:///./jarvis_users.db"

# SQLAlchemy "dvijogi"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Har bir sessiya uchun SessionLocal klassi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modellarimiz uchun asosiy klass
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()