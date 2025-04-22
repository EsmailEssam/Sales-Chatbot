from pydantic import BaseModel, ValidationError
from typing import List, Optional

class EndPointJsonSchema(BaseModel):
    data : dict
    event_type : str
    timestamp : str
    
   