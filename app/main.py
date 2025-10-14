from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .api import auth_router, user_router, category_router, budget_router, expense_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Money Manager API",
    description="A personal finance management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(category_router)
app.include_router(budget_router)
app.include_router(expense_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Money Manager API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}