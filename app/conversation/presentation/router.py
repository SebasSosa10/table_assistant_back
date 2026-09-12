from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from conversation.application.close_conversation import CloseConversation
from conversation.application.create_conversation import CreateConversation
from conversation.application.get_conversation import GetConversation
from conversation.application.send_message import SendMessage
from conversation.domain.ports.assistant_port import AssistantPort
from conversation.domain.ports.conversation_repository import ConversationRepository
from conversation.domain.ports.message_repository import MessageRepository
from conversation.infrastructure.ai.openrouter_assistant import OpenRouterAssistant
from conversation.infrastructure.repositories.conversation_repository_impl import (
    ConversationRepositoryImpl,
)
from conversation.infrastructure.repositories.message_repository_impl import (
    MessageRepositoryImpl,
)
from conversation.presentation.schemas.conversation_schema import (
    ConversationCreateSchema,
    ConversationResponseSchema,
    MessageCreateSchema,
    SendMessageResponseSchema,
    MessageResponseSchema,
)
from db.session import get_db
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from restaurant.infrastructure.repositories.restaurant_repository_impl import (
    RestaurantRepositoryImpl,
)
from shared.exceptions import AssistantError, ConflictError, NotFoundError
from table.domain.ports.table_repository import TableRepository
from table.infrastructure.repositories.table_repository_impl import TableRepositoryImpl
from user.domain.ports.user_repository import UserRepository
from user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter(prefix="/conversations", tags=["conversations"])


def get_conversation_repository(session: Session = Depends(get_db)) -> ConversationRepository:
    return ConversationRepositoryImpl(session)


def get_message_repository(session: Session = Depends(get_db)) -> MessageRepository:
    return MessageRepositoryImpl(session)


def get_restaurant_repository(session: Session = Depends(get_db)) -> RestaurantRepository:
    return RestaurantRepositoryImpl(session)


def get_table_repository(session: Session = Depends(get_db)) -> TableRepository:
    return TableRepositoryImpl(session)


def get_user_repository(session: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(session)


def get_assistant() -> AssistantPort:
    return OpenRouterAssistant()


@router.post("", response_model=ConversationResponseSchema, status_code=status.HTTP_201_CREATED)
def create_conversation(
    payload: ConversationCreateSchema,
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
    table_repository: TableRepository = Depends(get_table_repository),
    user_repository: UserRepository = Depends(get_user_repository),
) -> ConversationResponseSchema:
    try:
        conversation = CreateConversation(
            conversation_repository,
            restaurant_repository,
            table_repository,
            user_repository,
        ).execute(
            restaurant_id=payload.restaurant_id,
            table_id=payload.table_id,
            user_id=payload.user_id,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return ConversationResponseSchema.from_entity(conversation)


@router.get("/{conversation_id}", response_model=ConversationResponseSchema)
def get_conversation(
    conversation_id: int,
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    message_repository: MessageRepository = Depends(get_message_repository),
) -> ConversationResponseSchema:
    try:
        conversation, messages = GetConversation(
            conversation_repository,
            message_repository,
        ).execute(conversation_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return ConversationResponseSchema.from_entity(conversation, messages)


@router.post("/{conversation_id}/messages", response_model=SendMessageResponseSchema)
def send_message(
    conversation_id: int,
    payload: MessageCreateSchema,
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
    message_repository: MessageRepository = Depends(get_message_repository),
    assistant: AssistantPort = Depends(get_assistant),
) -> SendMessageResponseSchema:
    try:
        user_message, assistant_message = SendMessage(
            conversation_repository,
            message_repository,
            assistant,
        ).execute(conversation_id, payload.content)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    except AssistantError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=exc.message,
        ) from exc
    return SendMessageResponseSchema(
        user_message=MessageResponseSchema.from_entity(user_message),
        assistant_message=MessageResponseSchema.from_entity(assistant_message),
    )


@router.patch("/{conversation_id}/close", response_model=ConversationResponseSchema)
def close_conversation(
    conversation_id: int,
    conversation_repository: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationResponseSchema:
    try:
        conversation = CloseConversation(conversation_repository).execute(conversation_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return ConversationResponseSchema.from_entity(conversation)
