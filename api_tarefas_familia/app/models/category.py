from sqlalchemy import Column, Integer, String
from app.database import Base


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(45), nullable=False)
