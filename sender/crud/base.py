from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel

from sender.model.base_class import Base   # TODO: Create Redis base class!?

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        FastAPI like style.

        **Parameters**

        * `model`: A redis_om HashModel class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def read(self, pk: Any) -> Optional[ModelType]:
        return self.model.get(pk)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        self.model(**obj_in_data)
        self.model.save()
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

    def delete(self, pk: Any) -> None:
        self.model.delete(pk)


# TODO: set expiration
# def set_ttl(redis_pk: str):
#     if settings.REDIS_STORAGE_TTL_SECONDS > 0:
#         model_to_expire = Model.get(redis_pk)
#         Model.db().expire(model_to_expire.key(), settings.REDIS_STORAGE_TTL_SECONDS)