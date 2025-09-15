from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import  Optional
from pydantic import BaseModel


class IPhoneSaleBase(BaseModel):
    customer_name: str = Field(max_length=100)
    phone_model: str
    color: str
    storage_gb: int
    price: float
    sale_date: date
    store_location: str = Field(max_length=100)

    @field_validator("phone_model")
    def validate_model(cls, v):
        allowed_models = ["iphone X","iphone 11","iphone 12","iphone 13", "iphone 14", "iphone 15","iphone 16"]
        if v not in allowed_models:
            raise ValueError(f"phone_model must be one of {allowed_models}")
        return v

    @field_validator("color")
    def validate_color(cls, v):
        allowed_colors = ["black", "white", "blue", "red", "green", "pink", "yellow", "purple"]
        if v not in allowed_colors:
            raise ValueError(f"color must be one of {allowed_colors}")
        return v

    @field_validator("storage_gb")
    def validate_storage(cls, v):
        if v not in [128, 256, 512, 1024]:
            raise ValueError("storage_gb must be 128, 256, 512, or 1024")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("price must be positive")
        return v

    @field_validator("sale_date")
    def validate_date(cls, v):
        if v > date.today():
            raise ValueError("sale_date cannot be in the future")
        return v


class IPhoneSaleCreate(IPhoneSaleBase):
    pass


class IPhoneSaleUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, max_length=100)
    phone_model: Optional[str] = None
    color: Optional[str] = None
    storage_gb: Optional[int] = None
    price: Optional[float] = None
    sale_date: Optional[date] = None
    store_location: Optional[str] = Field(None, max_length=100)


class IPhoneSaleResponse(IPhoneSaleBase):
    id: int

    class Config:
        from_attributes = True
