from pydantic import BaseModel, ConfigDict


class CreatePostDTO(BaseModel):
    title: str
    body: str
    author_id: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class CreateCategoryDTO(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class PostDTO(BaseModel):
    id: int
    title: str
    body: str
    route_id: int
    category_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class PostPut(BaseModel):
    title: str
    body: str
    category_id: int


class CategoryPut(BaseModel):
    name: str
