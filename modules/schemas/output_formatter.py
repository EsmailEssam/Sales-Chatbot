from pydantic import BaseModel, Field
from typing import List, Optional

class ProductSuggestion(BaseModel):
    product_id: str = Field(
        description="Unique identifier for the product being suggested should be a number (e.g., '1')"
    )
    caption: str = Field(
        description="Brief explanation of why this product is being recommended"
    )

class ResponseContent(BaseModel):
    text: str = Field(...,
        description="Main response text containing product recommendations and information"
    )
    suggestions: List[ProductSuggestion] = Field(
        default=[],
        description="List of specific product suggestions related to the customer's query"
    )

class ResponseModel(BaseModel):
    response: ResponseContent = Field(
        description="Container for the response content and product suggestions"
    ) 
    session_id: str = Field(
        description="Unique identifier for the session" , default='1'
    )
