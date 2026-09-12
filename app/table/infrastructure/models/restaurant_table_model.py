from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class RestaurantTableModel(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    number = Column(String)
    label = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    restaurant = relationship("RestaurantModel", back_populates="tables")
    conversations = relationship("ConversationModel", back_populates="table")
