from pydantic import BaseModel, Field, field_validator


class CurrencyBase(BaseModel):
    name: str = Field(min_length=3, max_length=50, examples=["United States dollar"],
                      description="Полное название валюты")
    code: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]+$",
                      examples=["USD"])
    sign: str = Field(min_length=1, max_length=3, examples=["$"])

    @field_validator("code")
    def code_to_upper(cls, v):
        return v.upper()


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyResponse(CurrencyBase):
    id: int
