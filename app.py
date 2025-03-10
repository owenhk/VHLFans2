import fastapi
from fastapi import Request

app = fastapi.FastAPI()


@app.post("/cheat_engine/fetch_answers")
async def get_vhl_answers(request: Request):
    pass
