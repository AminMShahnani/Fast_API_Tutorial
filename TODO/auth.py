from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import models

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

app = FastAPI()