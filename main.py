from fastapi import FastAPI
import uvicorn
from src.routers import products
from src.routers import customers
from src.routers import orders
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.database.connection import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # This will safely create tables if they don't exist yet
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Inventory & Order Management API",lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows any frontend to connecttouc
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the router
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "UP", "message": "API is running smoothly."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)