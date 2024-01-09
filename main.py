import uvicorn
from fastapi import FastAPI
from handler.event_handlers import startup, shutdown
from router.router import router


app = FastAPI()

app.include_router(router, tags=["Tweet", "User"], prefix="/api/app")
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080, )
