from fastapi import FastAPI
import uvicorn
from src.routers import products # Import the router
from src.routers import customers
from src.routers import orders
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Inventory & Order Management API",
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