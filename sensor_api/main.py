import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sensor_api.presentation.routes import router
from sensor_api.infrastructure.database import DatabaseSingleton

app = FastAPI(title="Sensor API - Posture Monitor")

# Habilitando CORS para permitir requisições do Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Na vida real, colocar a URL do Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    if not os.getenv("TESTING"):
        db = DatabaseSingleton()
        db.create_tables()
