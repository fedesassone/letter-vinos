from sqlalchemy.orm import Session
from . import models, schemas

def get_wines(db: Session):
    return db.query(models.Wine).all()

def create_wine(db: Session, wine: schemas.WineBase):
    db_wine = models.Wine(**wine.dict())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine

def create_review(db: Session, wine_id: int, review: schemas.ReviewCreate):
    db_review = models.Review(wine_id=wine_id, content=review.content)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review