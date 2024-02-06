from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime
from typing import Any
from pydantic_core import core_schema, CoreSchema
from pydantic.annotated_handlers import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> CoreSchema:
        def validate(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)
        
        return core_schema.no_info_plain_validator_function(
            function=validate,
            serialization=core_schema.to_string_ser_schema(),
        )
    

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    
    class Config:
        json_encoders = {ObjectId: str}


class CommentBase(BaseModel):
    publication_date: datetime = Field(default_factory=datetime.now)
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    pass


class PostBase(MongoBaseModel):
    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)


class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PostCreate(PostBase):
    pass


class Post(PostBase):
    comments: list[Comment] = Field(default_factory=list)
