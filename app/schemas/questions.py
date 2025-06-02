from pydantic import BaseModel, Field
from typing import Optional

class QuestionCreate(BaseModel):
    text: str = Field (..., min_length=12)
    category_id: int = Field (..., description="ID категории вопроса")

class MessageResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    text: str
    category_id: int
    category: Optional[CategoryBase]

    class Config:
        # Указываем Pydantic использовать эти параметры чтобы можно было переносить данные прямо с объекта
        from_attributes = True

