from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

# Import our DB dependency, Models, and DTOs
from src.database.connection import get_db
from src.models.product import Product
from src.schemas.product import ProductCreate, ProductResponse

# Equivalent to @RestController and @RequestMapping("/products")
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Equivalent to @PostMapping
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check for SKU uniqueness
    query = select(Product).where(Product.sku == product_in.sku)
    result = await db.execute(query)
    existing_product = result.scalars().first()

    if existing_product:
        # Equivalent to throwing a ResponseStatusException
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with SKU '{product_in.sku}' already exists."
        )

    # 2. Map DTO to Entity
    new_product = Product(**product_in.model_dump())

    # 3. Save to database
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product) # Reloads the entity to get the generated ID and timestamps

    return new_product

# Equivalent to @GetMapping
@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    query = select(Product)
    result = await db.execute(query)
    products = result.scalars().all()
    return products

# Equivalent to @GetMapping("/{id}")
@router.get("/{id}", response_model=ProductResponse)
async def get_product_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.id == id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    return product

# Equivalent to @PutMapping("/{id}")
@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: UUID, product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    # 1. Fetch existing product
    query = select(Product).where(Product.id == id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    # 2. Check if the new SKU belongs to another product
    if product_in.sku != product.sku:
        sku_query = select(Product).where(Product.sku == product_in.sku)
        sku_result = await db.execute(sku_query)
        if sku_result.scalars().first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SKU already in use.")

    # 3. Update fields (Mapping DTO to Entity)
    for key, value in product_in.model_dump().items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)

    return product

# Equivalent to @DeleteMapping("/{id}")
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.id == id)
    result = await db.execute(query)
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    await db.delete(product)
    await db.commit()
    return None