from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    phone_number: str

class UserResponse(BaseModel):
    id: str
