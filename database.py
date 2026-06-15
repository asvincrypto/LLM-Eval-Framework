from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class EvalResult(Base):
    __tablename__ = "eval_results"

    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    model_version = Column(String)
    benchmark_name = Column(String)
    prompt = Column(Text)
    response = Column(Text)
    score = Column(Float)
    latency_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine("sqlite:///eval_results.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()