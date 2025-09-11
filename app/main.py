from fastapi import FastAPI
from . import models, database
from .routes import router as sales_router

app = FastAPI(title="iPhone Sales Tracker")

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

app.include_router(sales_router)