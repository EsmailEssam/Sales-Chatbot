"""
Helper function to convert product JSON data to a pandas DataFrame.
"""

import json
import pandas as pd
from pathlib import Path

def convert_json_to_df() -> pd.DataFrame:
    """
    Convert the products JSON file to a pandas DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame containing product information
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent.parent
    json_file = project_root / "products.json"
    
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df 