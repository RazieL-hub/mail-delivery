from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    user_id: int = Field(..., )
    email: EmailStr = None
    telegram: str = Field(None, )
    viber: str = Field(None, )
    whats_app: str = Field(None, )


class UserUpdateSchema(BaseModel):
    email: EmailStr = None
    telegram: str = Field(None, )
    viber: str = Field(None, )
    whats_app: str = Field(None, )
