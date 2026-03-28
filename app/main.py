from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth API", 
    description="Production Grade SignUp & LogIn",
    version="1.0.0")

app.include_router(auth.authrouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome To User Authentication System"}

@app.get("/health", tags=["Health"])
def health():
    return {"status":"ok"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="Auth API",
        version="1.0.0",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi_schema = None
app.openapi = custom_openapi