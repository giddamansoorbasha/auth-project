from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API", 
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.authrouter)

@app.get("/", response_class=FileResponse)
def serve_ui():
    return "index.html"

@app.get("/health", tags=["Health"])
def health():
    return {"status":"ok"}
