from typing import Self, Union, Dict

from redis_om import HashModel

from sender.model.redis_connector import get_redis_db


class Base(HashModel):
    ...

    # version with CRUD is not working

    def create(self, ttl_seconds=0) -> Self:
        self.connect()
        self.save()
        if ttl_seconds:
            self.set_ttl(pk=self.pk, ttl_seconds=ttl_seconds)
        return self

    # def update(
    #     self,
    #     db_obj: Self,
    #     obj_in: Union[UpdateSchemaType, Dict[str, int | str]],
    # ) -> Self:
    #     obj_data = obj_in.dict()
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     for field in obj_data:
    #         if field in update_data:
    #             setattr(db_obj, field, update_data[field])
    #     self.save()
    #     return self

    def set_ttl(self, pk: str, ttl_seconds=0):
        if ttl_seconds > 0:
            model_to_expire = self.get(pk)
            self.db().expire(model_to_expire.key(), ttl_seconds)

    def connect(self):
        self.Meta.database = get_redis_db()
