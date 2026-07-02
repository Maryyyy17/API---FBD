from fastapi import FastAPI
from crud_DONO import router as dono_router
from crud_RECEITA import router as receita_router

app = FastAPI(
    title = "API ITEM NEXUS",
    version = "0.0.1"
)

app.include_router(dono_router, prefix="/dono")
app.include_router(receita_router, prefix="/receita")