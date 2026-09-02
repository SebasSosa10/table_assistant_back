from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    phone = Column(String)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    restaurant = relationship("RestaurantModel", back_populates="users")
