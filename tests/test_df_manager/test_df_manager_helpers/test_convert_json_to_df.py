import pytest
import os
import json
import pandas as pd
from pydantic import ValidationError
from src.df_manager.df_manager_helpers.convert_json_to_df import ConvertJsonToDf
from src.schemas.end_point_json_schema import EndPointJsonSchema
from src.schemas.products_from_end_point_schema import Product


# Helper function to create sample JSON file with valid schema
def create_valid_json_file(tmp_path):
    data = {
        "data": {
            "products": [
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
        },
        "event_type": "product_update",
        "timestamp": "2024-01-01T00:00:00Z"
    }
    file_path = tmp_path / "products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return file_path, data


def test_read_json_file_success(tmp_path):
    """Test reading a valid JSON file with correct schema"""
    file_path, expected_data = create_valid_json_file(tmp_path)
    converter = ConvertJsonToDf(str(file_path))
    
    converter.read_json_file()
    assert converter.data is not None
    assert "products" in converter.data["data"]
    assert isinstance(converter.validated_data, dict)
    assert "event_type" in converter.validated_data


def test_read_json_file_not_found():
    """Test handling of non-existent file"""
    converter = ConvertJsonToDf("non_existent_file.json")
    with pytest.raises(FileNotFoundError):
        converter.read_json_file()


def test_read_json_file_invalid_format(tmp_path):
    """Test handling of invalid JSON format"""
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("this is not json", encoding="utf-8")
    
    converter = ConvertJsonToDf(str(invalid_file))
    with pytest.raises(json.JSONDecodeError):
        converter.read_json_file()


def test_read_json_file_invalid_schema(tmp_path):
    """Test handling of JSON with invalid schema"""
    bad_data = {
        "data": {
            "products": [
                {"invalid_key": "value"}  # Missing required fields
            ]
        }
    }
    bad_file = tmp_path / "bad.json"
    with open(bad_file, "w", encoding="utf-8") as f:
        json.dump(bad_data, f)

    converter = ConvertJsonToDf(str(bad_file))
    with pytest.raises(ValidationError):
        converter.read_json_file()


def test_read_json_file_missing_required_structure(tmp_path):
    """Test handling of JSON missing required structure"""
    bad_data = {"unexpected_key": []}
    bad_file = tmp_path / "bad.json"
    with open(bad_file, "w", encoding="utf-8") as f:
        json.dump(bad_data, f)

    converter = ConvertJsonToDf(str(bad_file))
    with pytest.raises(ValidationError):
        converter.read_json_file()


def test_get_products_from_json(tmp_path):
    """Test extracting products from validated JSON"""
    file_path, expected_data = create_valid_json_file(tmp_path)
    converter = ConvertJsonToDf(str(file_path))
    converter.read_json_file()
    
    products = converter.get_products_from_json()
    assert isinstance(products, list)
    assert len(products) == len(expected_data["data"]["products"])
    assert all(isinstance(product, dict) for product in products)
    assert all("product_id" in product for product in products)


def test_validate_products_keys(tmp_path):
    """Test validation of individual product keys"""
    file_path, _ = create_valid_json_file(tmp_path)
    converter = ConvertJsonToDf(str(file_path))
    converter.read_json_file()
    products = converter.get_products_from_json()
    
    validated_products = converter._validate_products_keys(products)
    assert isinstance(validated_products, list)
    assert all(isinstance(product, dict) for product in validated_products)
    assert all("product_id" in product for product in validated_products)


def test_run_returns_dataframe(tmp_path):
    """Test complete conversion process returning valid DataFrame"""
    file_path, expected_data = create_valid_json_file(tmp_path)
    converter = ConvertJsonToDf(str(file_path))

    df = converter.run()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == len(expected_data["data"]["products"])
    assert all(col in df.columns for col in ["product_id", "name", "description", "price", "category"])
    assert df["product_id"].dtype == "int64"
    assert df["price"].dtype == "float64"
    assert isinstance(df["category"].iloc[0], list)
