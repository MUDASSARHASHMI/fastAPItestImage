#Import the API router class from FastAPI
from fastapi import APIRouter
# Import the products routed from the 'app.api.v1.endpoints' module
from app.api.v1.endpoints import products
# Create an instance of the API Router
router = APIRouter()
# Include the 'products' router as a sub-router under the '/product'/ prefix
# and add assign tag "Products" to the group related to the Endpoint
router.include_router(products.router, prefix="/products", tags=["Products"])
