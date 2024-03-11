from api.routers import event as event_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(event_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
