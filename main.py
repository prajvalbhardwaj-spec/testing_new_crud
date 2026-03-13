from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine, Base, SessionLocal
from app.routers import auth, users, blogs
from app import seed as seeder


# ---------------------------------------------------------------------------
# Lifespan: create tables + auto-seed on startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    # Seed dummy data on first run
    db = SessionLocal()
    try:
        seeder.seed(db)
    finally:
        db.close()

    yield  # app runs here


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Blog API",
    description="A FastAPI blog application with user authentication and CRUD operations.",
    version="1.0.0",
    lifespan=lifespan
)

# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)

# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    return {"message": "API is running"}


# ---------------------------------------------------------------------------
# Manual seed endpoint (backup for deployed DB)
# ---------------------------------------------------------------------------

@app.post("/seed", tags=["Health"])
def manual_seed():
    db = SessionLocal()
    try:
        seeded = seeder.seed(db)
        if seeded:
            return {"message": "Database seeded!"}
        return {"message": "Already seeded, skipping"}
    finally:
        db.close()
