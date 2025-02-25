from typing import  List
from pydantic import BaseModel , Field
from typing import List


class SingleExtractedBook(BaseModel):
    Book_title: str = Field(..., title="The title of the book")
    Book_author: str = Field(..., title="The author of the book")
    Year_of_publication: str = Field(..., title="The publication year of the book")
    Publisher: str = Field(..., title="The publisher of the book")
    price: float = Field(..., title="The current price of the book")
    discount_percentage: float = Field(title="The discount percentage on the book. Set to None if no discount", default=None)
    price_after_discount: float = Field(title="The final price after applying the discount. Set to None if no discount", default=None)
    Image_URL: str = Field(title="The cover image URL of the book", default=None)

    agent_recommendation_rank: int = Field(..., title="The book's rank in the recommendation list (out of 5, Higher is Better)")
    agent_recommendation_notes: List[str] = Field(..., title="Reasons why this book is recommended or not compared to others")
    

class AllExtractedBooks(BaseModel):
    books: List[SingleExtractedBook]

        
class Consultantion(BaseModel):
    personalized_sales_assistance: str = Field(..., title="Personalized sales assistance")
    book_recommendations: AllExtractedBooks = Field(title="Book recommendations based on user preferences", default=None)