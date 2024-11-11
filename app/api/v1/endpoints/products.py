from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from app.schema.product import Product, ProductCreate, ProductPatch, ProductUpdate

from app.api.deps import get_db
from app import crud

# Create an APIRouter Instance
router = APIRouter()

# Define a route to create a new Product
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)],product_in: ProductCreate):
    # Use the CRUD (Create, Read, Update, Delete)
    # to create a new product or return an existing one if it already exists
    product, createed = await crud.product.get_or_create(
        db=db, defaults=product_in.dict()
    )
    if not createed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Product Exists'
        )
    # Return the created or existing product
    return Product
@router.get("/{productId}", response_model=Product, status_code=HTTP_200_OK)
async def get_product(
        db:Annotated[AsyncSession, Depends(get_db)],
        productId: str):
    # Use the CRUD operation to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id = productId)
    if not product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Product not found')
    return product
# Define a route to retrieve a paginated list of Products
@router.get('/', response_model=Page[Product], status_code=status.HTTP_200_OK)
async def get_products(db:Annotated[AsyncSession, Depends(get_db)], skip: int=0, limit:int=20):
    products = await crud.product.get_multi(db=db, skip=skip, limit=limit):
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Products not found')
    return paginate(products)
# Define a route to partially update the Product
@router.patch("/{productId}", status_code=status.HTTP_200_OK)
async def patch_product(db: Annotated[AsyncSession, Depends(get_db)], product_Id: str, product_in: ProductPatch):
    # Use the CRUD operations to retrieve a product by its ID
    product = await crud.product.get(db=db, obj_id=product_Id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')
    product_patched = await crud.product.patch(db=db, obj_id=product_Id, obj_in=product_in.dict())
    return product_patched
# Define a route to fully update a product



