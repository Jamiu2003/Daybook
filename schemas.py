from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime, date

class TodoCreate(BaseModel):
    title:str
    description: str|None = None

class GetTodo(BaseModel):
    id:int
    title:str
    description: str| None = None
    time_created: datetime

    model_config = ConfigDict(from_attribute = True)

class TodoUpdate(BaseModel):
    title:str|None = None
    description:str | None = None
    completed:bool | None = None

    model_config = ConfigDict(from_attributes=True)

class UserRegisteration(BaseModel):
    username:str
    email: EmailStr
    password:str
    full_name:str

    @field_validator("full_name")
    @classmethod
    def letters_only(cls, v):
        if not v.replace(" ", ""):
            raise ValueError("Full name can only contain letters and spaces")
        return v

class UserLogin(BaseModel):
    username:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:str

class EntryCreate(BaseModel):
    content:str
    mood:str | None = None

class EntryResponse(BaseModel):
    id:int
    content:str
    mood:str|None
    time_created: datetime

    model_config = ConfigDict(from_attributes=True)


class MilestoneCreate(BaseModel):
    title:str
    

    #model_config = ConfigDict(from_attributes =True)
class MilestoneUpdate(BaseModel):
    completed: bool


class MilestoneResponse(BaseModel):
    id:int
    title:str
    completed:bool
    time_created: datetime

class GoalCreate(BaseModel):
    title:str
    target_date:date | None = None
    

    #model_config = ConfigDict(from_attributes = True)

class GoalResponse(BaseModel):
    id:int
    title:str
    target_date:date | None
    time_created: datetime
    milestones: list[MilestoneResponse] = []
    model_config = ConfigDict(from_attributes = True)

    



