import fastapi
from fastapi import Request
from contextlib import asynccontextmanager
import asyncpg
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from playwright.async_api import Playwright, async_playwright
from AIEngine import agent
from defs import VHLFans, Input

load_dotenv()

# Create a FastAPI object with a init



@asynccontextmanager
async def lifespan(service: VHLFans):
    # Code to run on startup, initialize the postgres connection pool
    print("Starting up...")
    pool_url = os.getenv("DATABASE_URL")
    service.con = await asyncpg.create_pool(pool_url,
                                            max_size=20)
    service.tcp_connector = aiohttp.TCPConnector(limit=50)
    service.pw = await async_playwright().start()
    yield
    # Code to run on shutdown
    print("Shutting down...")


app: fastapi.FastAPI = VHLFans(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cheat_engine/classic_cheat")
async def get_vhl_answers(request: Request):
    request_body = await request.json()  # Fetch the request body
    input_obj = Input.model_validate(request_body)
    solution = await agent.start_ai_solver(input_obj, request.app)
    return solution.model_dump()
    