from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os, csv

from . import models, schemas, crud, database

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    # Ensure schema exists (safe if already created)
    models.Base.metadata.create_all(bind=database.engine)

    # Load wines from CSV
    csv_path = os.path.join(os.path.dirname(__file__), "..", "demo.csv")
    if os.path.exists(csv_path):
        db = database.SessionLocal()
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row["name"].strip()
                image_url = row["image"].strip()
                if not db.query(models.Wine).filter_by(name=name).first():
                    wine_data = schemas.WineBase(
                        name=name,
                        description=f"A fine {name} wine.",
                        image_url=image_url
                    )
                    crud.create_wine(db, wine_data)
        db.close()
        print("✅ Wines loaded from demo.csv.")
    else:
        print("⚠️ demo.csv not found at project root.")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    wines = crud.get_wines(db)
    return templates.TemplateResponse("index.html", {"request": request, "wines": wines})

@app.post("/review/{wine_id}")
def add_review(wine_id: int, content: str = Form(...), db: Session = Depends(get_db)):
    crud.create_review(db, wine_id, schemas.ReviewCreate(content=content))
    return RedirectResponse("/", status_code=303)