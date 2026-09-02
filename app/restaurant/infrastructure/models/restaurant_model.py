from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.database import Base


class RestaurantModel(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)

    users = relationship("UserModel", back_populates="restaurant")
