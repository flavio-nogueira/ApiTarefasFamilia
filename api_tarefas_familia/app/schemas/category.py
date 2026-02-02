from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    category_name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None


class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True
