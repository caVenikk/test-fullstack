from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    description: str

    class Config:
        from_attributes = True


class ProductSchema(ProductBaseSchema):
    id: int
