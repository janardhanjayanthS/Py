import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.config import lifespan
from src.core.excptions import WeakPasswordException

from .routes import category, product, user

app = FastAPI(lifespan=lifespan)

app.include_router(product.product)
app.include_router(user.user)
app.include_router(category.category)


@app.exception_handler(WeakPasswordException)
async def handle_weak_password(request: Request, error: WeakPasswordException):
    return JSONResponse(
        status_code=400, content={"status": "Error", "message": error.message}
    )


@app.get("/")
def home():
    return {"jello": "world"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
