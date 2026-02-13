import os

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from file import Base

# pega caminho do DB do ambiente
db_path = os.getenv("SQLITE_DB_PATH", "instance/wrfem_blobs.db")

# cria engine SQLite
engine = create_engine(f"sqlite:///{db_path}", echo=True, future=True)
Base.metadata.create_all(engine)

# executa PRAGMA no connect
with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL"))
    conn.execute(text("PRAGMA synchronous=NORMAL"))

# cria session factory (ORM)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# exemplo de uso
with SessionLocal() as session:
    result = session.execute(text("SELECT 1"))
    print(result.scalar_one())


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection):
    with dbapi_connection.cursor() as cursor:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()
