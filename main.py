from bson import ObjectId
from fastapi import FastAPI
from handler.event_handlers import startup, shutdown
from router.router import router


app = FastAPI()
app.include_router(router, tags=["User", "Tweet"], prefix="/api/app")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)