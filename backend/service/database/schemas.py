from pydantic import BaseModel


class ORMModel(BaseModel):
    class Config:
        orm_mode = True


class CategoryModel(ORMModel):
    id: int
    name: str
