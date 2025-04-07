import fastapi
from pydantic import BaseModel, Field
import os
import asyncpg
import aiohttp
import openai
from typing import Optional


class VHLFans(fastapi.FastAPI):
    def __init__(self, *args, **kwargs):
        self.con: Optional[asyncpg.Pool] = kwargs.pop("con", None)
        super().__init__(*args, **kwargs)
        self.tcp_connector: Optional[aiohttp.TCPConnector] = None
        self.ai = openai.AsyncClient(api_key=os.getenv("OPENAI_API_KEY"))
        self.serp_api_key = os.getenv("SERP_API_KEY")
        self.scraper_api_key = os.getenv("SCRAPER_API_KEY")

class Question(BaseModel):
    id: str = Field(default_factory=lambda: os.urandom(32).hex())
    selector: str
    type: str
    question: str
    options: Optional[list[str]] = None

class Input(BaseModel):
    questions: list[Question]
    lesson_id: str
    lesson_name: str
    unit: str

class QuizletFlashcard(BaseModel):
    front: str
    back: str

class QuizletDeck(BaseModel):
    flashcards: list[QuizletFlashcard]
