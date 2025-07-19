# src/currency_exchange_app/middlewares.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.currency_exchange_app.exceptions import AppBaseException


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def custom_exception_handler(request: Request, exc: AppBaseException):
    return exc.to_response()
