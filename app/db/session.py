import time

from sqlalchemy.exc import OperationalError

from db.database import Base, SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from conversation.infrastructure.models.conversation_model import ConversationModel  # noqa: F401
    from conversation.infrastructure.models.message_model import MessageModel  # noqa: F401
    from restaurant.infrastructure.models.restaurant_model import RestaurantModel  # noqa: F401
    from table.infrastructure.models.restaurant_table_model import RestaurantTableModel  # noqa: F401
    from user.infrastructure.models.user_model import UserModel  # noqa: F401

    for attempt in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except OperationalError:
            if attempt == 9:
                raise
            time.sleep(2)
