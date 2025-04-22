from pydantic import BaseModel, ValidationError
from typing import List, Optional

class Product(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    category: List
    concerns: List
    ingredients: List[str]
    product_file: Optional[str] = None
    best_seller: bool
    new_arrived: bool
   