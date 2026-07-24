from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import DomainError, UserNotFoundError
from src.infrastructure.repositories import JsonUserRepository

app = FastAPI(title="SafeCore API", version="1.0.0")

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": "Not Found", "message": str(exc)},
    )

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=400,
        content={"error": "Business Rule Violation", "message": str(exc)},
    )

@app.get("/")
def health_check():
    return {"status": "SafeCore running successfully"}