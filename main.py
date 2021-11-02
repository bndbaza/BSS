from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import  database
from routers import entry, output, contract

app = FastAPI()
app.state.database = database

origins = [
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://192.168.0.75:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(entry.router)
app.include_router(output.router)
app.include_router(contract.router)