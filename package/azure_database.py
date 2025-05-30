from azure.identity import DefaultAzureCredential
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from package.configurations.config import conn_str

# Azure token credential
credential = DefaultAzureCredential()


engine = create_engine(conn_str, echo=True, future=True, pool_size=10, max_overflow=20)
# engine = create_engine("sqlite://")


# SQLAlchemy ORM base + session
class Base(DeclarativeBase):
    pass


SessionFactory = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)
Session = scoped_session(SessionFactory)


# Sesion for AZURE SQLDB
def get_session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()
