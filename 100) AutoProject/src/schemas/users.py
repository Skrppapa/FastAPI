from pydantic import BaseModel, Field, ConfigDict

class MetaSchema(BaseModel):
    id: int = Field(ge = 1)

class UserSchema(MetaSchema):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    age: int = Field(gt = 18)
    credit_rating: int = Field(gt = 1, le = 10)
    work_place: str | None = Field(max_length=100)

    model_config = ConfigDict(extra="forbid")