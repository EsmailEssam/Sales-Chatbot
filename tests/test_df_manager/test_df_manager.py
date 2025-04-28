import pytest
import pandas as pd
from src.df_manager.df_manager import DfManager
from pathlib import Path
import json

VALID_PRODUCTS = [
    
    
    {   
                "product_id": 1,
                "name": "Herforte Lotion Spray (to fill in gaps and treat alopecia)",
                "description": "Hair forte is a mixture of natural extracts and extracts of the most important hair oils with anti-dandruff agent, to be a quick treatment for hair loss, guaranteed and tested by dermatologists for fortifying hair & increase hair shaft strength to prevent hair loss. Also, Hair forte spray stimulates hair germination to be an effective solution to fill the frontal spaces in women and men, in addition to treating dandruff & itching associated with dryness and inflammation of the scalp, Hair forte spray is suitable for all hair types even oily & dry scalp.\r\n\r\nComposition:-\r\nHair forte spray with its unique formula to be effective in stimulating the blood circulation of the scalp and hair follicles to strengthen and nourish them to prevent hair loss and also to stimulate root germination for the growth of healthy, thick, long and strong hair without dandruff.\r\n\r\n\u2022\tJojoba Oil Extract.\r\n\u2022\tGarlic Oil Extract.\r\n\u2022\tNigella.\r\n\u2022\tRosemary.\r\n\u2022\tCaffeine.\r\n\u2022\tThyme Oil.\r\n\u2022\tSalicylic acid.\r\n\u2022\tPanthenol.\r\n\u2022\tAloe Vera.\r\n\u2022\tVitamin E.\r\nIndicated for:\r\n*Diffuse hair fall.\r\n*Adjuvant therapy for alopecia areata. \r\n*Controls split ends, roughness, dryness& brittleness of hair. \r\n*Controls dandruff.\r\n\r\nApplication:\r\nSpray onto wet or dry hair& scalp \u201c6 pump\u201d suitable amount then massage& style as usual, once or twice daily preferably start from the forehead to back of the head in a circular movement or as directed by physician.\r\n\r\nPackage:\r\n 120 ml.",
                "ingredients": [
                    "Jojoba Oil Extract",
                    "Garlic Oil Extract",
                ],
                "concerns": [
                    [
                        "Hair loss"
                    ]
                ],
                "category": [
                    "Hair Care",
                    "Hair spray& lotion"
                ],
                "price": "200.00",
                "product_file": None,
                "best_seller": True,
                "new_arrived": False
            }
]

def create_json_file(tmp_path: Path, data: list) -> Path:
    path = tmp_path / "products.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "event_type": "products.updated",
            "timestamp": "2025-04-21T15:24:17.441205Z",
            "data": {"products": data}
        }, f, indent=4)
    return path

def test_df_manager_initialization_success(tmp_path):
    file_path = create_json_file(tmp_path, VALID_PRODUCTS)
    manager = DfManager(str(file_path))
    assert isinstance(manager.df, pd.DataFrame)
    assert not manager.df.empty

def test_get_category_set(tmp_path):
    file_path = create_json_file(tmp_path, VALID_PRODUCTS)
    manager = DfManager(str(file_path))
    category_set = manager.get_category_set()
    assert category_set == {"Hair Care"  , "Hair spray& lotion"}

def test_get_concerns_set(tmp_path):
    file_path = create_json_file(tmp_path, VALID_PRODUCTS)
    manager = DfManager(str(file_path))
    concerns_set = manager.get_concerns_set()
    assert concerns_set == {"Hair loss"}

def test_get_ingredients_set(tmp_path):
    file_path = create_json_file(tmp_path, VALID_PRODUCTS)
    manager = DfManager(str(file_path))
    ingredients_set = manager.get_ingredients_set()
    assert ingredients_set == {"Garlic Oil Extract", "Jojoba Oil Extract"}

def test_get_cleaned_df(tmp_path):
    file_path = create_json_file(tmp_path, VALID_PRODUCTS)
    manager = DfManager(str(file_path))
    cleaned_df = manager.get_cleaned_df()
    assert isinstance(cleaned_df, pd.DataFrame)
    assert not cleaned_df.empty
