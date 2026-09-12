from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String)
    status = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    messages = relationship("MessageModel", back_populates="conversation")
    user = relationship("UserModel", back_populates="conversations")
    table = relationship("RestaurantTableModel", back_populates="conversations")
