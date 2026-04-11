"""Auth request/response schemas."""

import uuid

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    agency_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    agency_id: uuid.UUID | None
    agency_role: str
    agency_name: str | None = None

    model_config = {"from_attributes": True}


class InviteRequest(BaseModel):
    email: EmailStr
    full_name: str
    agency_role: str = "recruiter"
