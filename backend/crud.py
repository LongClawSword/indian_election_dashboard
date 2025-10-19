import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import ElectionResult

CSV_PATH = "election_data.csv"

def load_csv_to_db(db: Session, csv_path=CSV_PATH):
    if db.query(ElectionResult).first():
        return

    df = pd.read_csv(csv_path)

    str_cols = ["state", "constituency", "candidate", "party", "gender",
                "education", "profession", "party_type"]
    for col in str_cols:
        df[col] = df[col].astype(str).fillna("Unknown").str.strip()

    numeric_cols = ["votes", "vote_share_percentage", "position", "margin", "margin_percentage"]
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    df["vote_share_percentage"] = pd.to_numeric(df["vote_share_percentage"], errors="coerce").fillna(0.0)
    df["position"] = pd.to_numeric(df["position"], errors="coerce").fillna(0).astype(int)
    df["margin"] = pd.to_numeric(df["margin"], errors="coerce").fillna(0).astype(int)
    df["margin_percentage"] = pd.to_numeric(df["margin_percentage"], errors="coerce").fillna(0.0)

    df["is_winner"] = df["position"] == 1

    for _, row in df.iterrows():
        record = ElectionResult(
            year=int(row["year"]),
            state=row["state"],
            constituency=row["constituency"],
            candidate=row["candidate"],
            party=row["party"],
            votes=row["votes"],
            vote_share_percentage=row["vote_share_percentage"],
            position=row["position"],
            margin=row["margin"],
            margin_percentage=row["margin_percentage"],
            gender=row["gender"],
            education=row["education"],
            profession=row["profession"],
            party_type=row["party_type"],
            is_winner=row["is_winner"]
        )
        db.add(record)

    db.commit()


def get_years(db: Session):
    return [y[0] for y in db.query(ElectionResult.year).distinct().order_by(ElectionResult.year).all()]

def get_elections_by_year(db: Session, year: int):
    results = db.query(ElectionResult).filter(ElectionResult.year == year).all()
    return [r.__dict__ for r in results]

def get_seat_share(db: Session, year: int):
    res = db.query(ElectionResult.party, func.count().label("seats")) \
            .filter(ElectionResult.year == year, ElectionResult.is_winner==True) \
            .group_by(ElectionResult.party).all()
    return [{"party": r.party, "seats": r.seats} for r in res]


def get_state_turnout(db: Session, year: int):
    res = db.query(ElectionResult.state, func.sum(ElectionResult.votes).label("votes")) \
            .filter(ElectionResult.year == year) \
            .group_by(ElectionResult.state).all()
    return [{"state": r.state, "votes": r.votes} for r in res]

def get_gender_trends(db: Session):
    res = db.query(ElectionResult.year, ElectionResult.gender, func.count().label("count")) \
            .group_by(ElectionResult.year, ElectionResult.gender) \
            .order_by(ElectionResult.year).all()
    return [{"year": r.year, "gender": r.gender, "count": r.count} for r in res]

def get_top_parties(db: Session, year: int, top_n=5):
    party_votes = db.query(
        ElectionResult.party,
        func.sum(ElectionResult.votes).label("total_votes")
    ).filter(
        ElectionResult.year == year
    ).group_by(
        ElectionResult.party
    ).subquery()

    total_votes = db.query(
        func.sum(ElectionResult.votes)
    ).filter(
        ElectionResult.year == year
    ).scalar()

    res = db.query(
        party_votes.c.party,
        (party_votes.c.total_votes / total_votes * 100).label("vote_share_percentage")
    ).order_by(
        desc("vote_share_percentage")
    ).limit(top_n).all()

    return [
        {"party": r.party, "vote_share_percentage": round(r.vote_share_percentage, 2)}
        for r in res
    ]

def get_margin(db: Session, year: int):
    res = db.query(ElectionResult.constituency, ElectionResult.state, ElectionResult.candidate, 
                   ElectionResult.party, ElectionResult.votes, ElectionResult.margin) \
            .filter(ElectionResult.year == year, ElectionResult.is_winner==True) \
            .all()
    return [{"constituency": r.constituency, "state": r.state, "candidate": r.candidate, 
             "party": r.party, "votes": r.votes, "margin": r.margin} for r in res]

def search_candidates(db: Session, year: int, query: str):
    like_query = f"%{query}%"
    res = db.query(ElectionResult) \
            .filter(ElectionResult.year == year) \
            .filter((ElectionResult.candidate.ilike(like_query)) | (ElectionResult.constituency.ilike(like_query))) \
            .all()
    return [r.__dict__ for r in res]
