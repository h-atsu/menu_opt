from fastapi import FastAPI
from routers import opt_menu
app = FastAPI()

app.include_router(opt_menu.router)
