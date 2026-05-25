from time import perf_counter

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

"""
http middleware - it is like a gaurd/security for all the routes, and I can
customize it to do whatever I want to a response. I can access all attrs of
a response. and include custom code.

this is how I can define a http middleware - in Fastapi

the call_next(request) -> calls the routes(endpoints)
lines above it are executed before hitting endpoint
lines after it are executed after hitting endpoint

the order of middleware is its definition order
"""


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request)
    response_time = perf_counter() - start
    response.headers["X-Process-Time"] = str(response_time)
    return response


@app.get("/")
async def home():
    return JSONResponse({"home": "route"})


if __name__ == "__main__":
    uvicorn.run(app)
