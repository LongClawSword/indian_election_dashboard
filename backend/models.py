from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class ElectionResult(Base):
    __tablename__ = "election_results"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    state = Column(String, index=True)
    constituency = Column(String, index=True)
    candidate = Column(String, index=True)
    party = Column(String, index=True)
    votes = Column(Integer)
    vote_share_percentage = Column(Float)
    position = Column(Integer)
    margin = Column(Integer)
    margin_percentage = Column(Float)
    gender = Column(String)
    education = Column(String)
    profession = Column(String)
    party_type = Column(String)
    is_winner = Column(Boolean)
