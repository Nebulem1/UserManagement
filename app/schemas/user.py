from datetime import datetime

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool | None = True


# Properties to run when creating user
class UserCreate(UserBase):
    password: str


# Properties for updating a user
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str


class UserRoleUpdate(BaseModel):
    role: str


# Properties returned to client
class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
