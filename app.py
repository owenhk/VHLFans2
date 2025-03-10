import fastapi
from fastapi import Request
from contextlib import asynccontextmanager
import asyncpg

# Create a FastAPI object with a init

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # Code to run on startup, initialize the postgres connection pool
    print("Starting up...")
    app.state.con = await asyncpg.create_pool("", max_size=20)
    yield
    # Code to run on shutdown
    print("Shutting down...")

app = fastapi.FastAPI(lifesan=lifespan)

@app.post("/cheat_engine/fetch_answers")
async def get_vhl_answers(request: Request):
    # Use WebEngine to decode the HTML of the page
    # Check CacheKit to see if the problem has already been solved
    # Use AIEngine to determine how to solve each set of questions
    # Pass AIEngine queries to QuizletEngine to get proper answers
    # Add a background worker to save results in CacheEngine
    # Pass the results back to the user, they cheated :)
    pass
