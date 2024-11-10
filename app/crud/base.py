from typing import Any, Dict, Generic, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import CreateEnumType
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.ddl import CreateSchema

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
           Generic CRUD (Create, Read, Update, Delete) operations for SQLAlchemy models.

        This class provides a set of generic CRUD operations that can be used with SQLAlchemy models.
        It includes methods for creating, retrieving, updating, and deleting records in the database.
        Args:
            model (Type[ModelType]): The SQLAlchemy model class to perform CRUD operations on.
        Example:
            To create a CRUD instance for a specific model (e.g., User model):
    ```python
            crud_user = CRUDBase[Prodcut, ProductCreateSchema, ProductUpdateSchema]
            ```
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model
    # Get single instance
    async def get(self, db: AsyncSession, obj_id: str)-> Optional[ModelType]:
        query = await db.execute(select(self.model).where(self.model.id == obj_id))
        return query.scalars().first()

    # Get all instances
    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> ModelType:
        query = await db.execute(select(self.model))
        return query.scalars().all()
    # Search a specific instance
    async def get_by_params(self, db: AsyncSession, **params: Any) -> Optional[ModelType]:
        query = select(self.model)
        for key, value in params.items():
            if isinstance(value, str):
                query = query.where(func.lower(getattr(self.model, key))==func.lower(value))
            else:
                query = query.where(getattr(self.model, key) == value)
        result = await db.execute(query)
        return result.scalar_one_or_none()
