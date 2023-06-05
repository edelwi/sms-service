from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from sender.model.base_class import Base  # TODO: Create Redis base class!?
from sender.crud.redis_connector import get_redis_db

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], ttl_second: int = 0):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        (FastAPI like style.)

        **Parameters**

        * `model`: A redis_om HashModel class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.ttl = ttl_second

        # Migrator().run()
        self.model.Meta.database = get_redis_db()

    def read(self, pk: str) -> Optional[ModelType]:
        return self.model.get(pk)

    def create(self, obj_in: CreateSchemaType, set_ttl=True) -> ModelType:
        obj_in_data = obj_in.dict()
        self.model(**obj_in_data)
        self.model.save()
        if set_ttl:
            self.set_ttl(pk=self.model.pk, ttl_seconds=self.ttl)
        return self.model

    def update(
        self,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = obj_in.dict()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        self.model.save()
        return self.model

    def delete(self, pk: str) -> None:
        self.model.delete(pk)

    def set_ttl(self, pk: str, ttl_seconds=0):
        if ttl_seconds > 0:
            model_to_expire = self.model.get(pk)
            self.model.db().expire(model_to_expire.key(), ttl_seconds)

