from pydantic import BaseModel

class ReviewBase(BaseModel):
    content: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    class Config:
        orm_mode = True

class WineBase(BaseModel):
    name: str
    description: str
    image_url: str

class Wine(WineBase):
    id: int
    reviews: list[Review] = []
    class Config:
        orm_mode = True