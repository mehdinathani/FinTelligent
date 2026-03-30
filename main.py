from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List

# 1. DATABASE SETUP
sqlite_url = "sqlite:///./fintelligent.db"
engine = create_engine(sqlite_url, echo=True)

# 2. MODEL (SQLModel = Pydantic + SQLAlchemy)
class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
    amount: float
    is_expense: bool

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 3. DEPENDENCY INJECTION (The "Depends" magic)
def get_session():
    with Session(engine) as session:
        yield session  # Yields session, auto-closes when request is done

app = FastAPI(title="FinTelligent API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# 4. CRUD ENDPOINTS
@app.post("/transactions/", response_model=Transaction)
def add_transaction(tx: Transaction, session: Session = Depends(get_session)):
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx

@app.get("/transactions/", response_model=List[Transaction])
def get_transactions(session: Session = Depends(get_session)):
    return session.exec(select(Transaction)).all()