from fastapi import FastAPI
from app.api import router
app = FastAPI(title="Financial Data Aggregator")
app.include_router(router)
#app.include_router(assets.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


