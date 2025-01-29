from fastapi import FastAPI
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from app.database import init_db
from app.routes import user, account, payment

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(account.router, prefix="/accounts", tags=["accounts"])
app.include_router(payment.router, prefix="/payments", tags=["payments"])


@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def root():
    return {"message": "Welcome to the banking system API!"}
