from fastapi import APIRouter

assistant = APIRouter()


@assistant.get("/assistant/", tags=["assistant"])
async def root():
    print("Hello from Warden!")
    return {"message": "Hello from Warden!"}
