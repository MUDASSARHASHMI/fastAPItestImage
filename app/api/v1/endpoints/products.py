from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from app.schema.product import Product, ProductCreate, ProductPatch, ProductUpdate