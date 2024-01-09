import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from handler.event_handlers import startup, shutdown
from router.router import router


async def ping():
    return {"Success": True}


app = FastAPI()
app.add_event_handler("startup", startup)
app.include_router(router, tags=["User", "Tweet"], prefix="/api/app")

app.add_event_handler("shutdown", shutdown)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080, )
