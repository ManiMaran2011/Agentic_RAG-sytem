from sqlalchemy import create_engine, Column, String, Text, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./govpreneurs.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(String, primary_key=True, index=True)
    draft = Column(Text)
    gaps = Column(Text)
    compliance_score = Column(Float)
    status = Column(String)
    version = Column(Integer)


def init_db():
    Base.metadata.create_all(bind=engine)