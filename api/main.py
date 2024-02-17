from fastapi import FastAPI
from routers import optimize_router
app = FastAPI()

app.include_router(optimize_router.router)
