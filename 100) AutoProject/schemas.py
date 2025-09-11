from pydantic import BaseModel, Field, ConfigDict

class MetaSchema(BaseModel):
    id: int = Field(ge = 1)
    
# Класс для валидации вытомобилей
class CarSchema(MetaSchema): 
    brand: str = Field(max_length=200) # Если мы не указываем | None то поле считается обязательным
    model: str = Field(max_length=200) 
    price: int = Field(gt = 0) # grated or equal (ge) больше или равен. less or equal (le) меньше или равен
    year_release: int = Field(gt = 1900)
    color: str = Field(max_length=100)
    added: str | None = Field(max_length=1000)

    model_config = ConfigDict(extra="forbid") # Буквально - запрети дополнительные параметры

class UserSchema(MetaSchema):
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    age: int = Field(gt = 18)
    credit_rating: int = Field(gt = 1, le = 10)
    work_plase: str | None = Field(max_length=100)

    model_config = ConfigDict(extra="forbid") # Буквально - запрети дополнительные параметры