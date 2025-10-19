# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Indian Election Dashboard API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Auto-load CSV on startup ---
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        crud.load_csv_to_db(db)
    finally:
        db.close()

# --- API Endpoints ---
@app.get("/api/years")
def api_years(db: Session = Depends(get_db)):
    return {"years": crud.get_years(db)}

@app.get("/api/elections/{year}")
def api_elections(year: int, db: Session = Depends(get_db)):
    return {"data": crud.get_elections_by_year(db, year)}

@app.get("/api/seat_share/{year}")
def api_seat_share(year: int, db: Session = Depends(get_db)):
    return {"seat_share": crud.get_seat_share(db, year)}

@app.get("/api/state_turnout/{year}")
def api_state_turnout(year: int, db: Session = Depends(get_db)):
    return {"turnout": crud.get_state_turnout(db, year)}

@app.get("/api/gender_trends")
def api_gender_trends(db: Session = Depends(get_db)):
    return {"trend": crud.get_gender_trends(db)}

@app.get("/api/top_parties/{year}")
def api_top_parties(year: int, top_n: int = 5, db: Session = Depends(get_db)):
    return {"top_parties": crud.get_top_parties(db, year, top_n)}

@app.get("/api/margin/{year}")
def api_margin(year: int, db: Session = Depends(get_db)):
    return {"margin": crud.get_margin(db, year)}

@app.get("/api/search")
def api_search(query: str, year: int, db: Session = Depends(get_db)):
    return {"results": crud.search_candidates(db, year, query)}
