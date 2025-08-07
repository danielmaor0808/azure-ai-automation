from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class UserInfo(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    id_number: Optional[str] = None
    gender: Optional[Literal["male", "female", "זכר", "נקבה"]] = None
    age: Optional[int] = Field(None, ge=0, le=120)
    hmo: Optional[Literal["מכבי", "מאוחדת", "כללית"]] = None
    card_number: Optional[str] = None
    membership_tier: Optional[Literal["זהב", "כסף", "ארד"]] = None

class ChatRequest(BaseModel):
    user_info: UserInfo
    history: List[str]
    message: str
    phase: Literal["info_collection", "qa"]

class ChatResponse(BaseModel):
    answer: str
    user_info: Optional[UserInfo] = None
    phase: Optional[str] = None
