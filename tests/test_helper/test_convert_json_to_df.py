import pytest
import pandas as pd
import json
import os
from modules.df_manager.convert_json_to_df import convert_json_to_df

@pytest.fixture
def sample_json_file(tmp_path):
    """Fixture to create a sample JSON file for testing."""
    data = {
        "event_type": "products.updated",
        "timestamp": "2025-04-17T15:39:22.403774Z",
        "data": {
            "products": [
                {
                    "product_id": 1,
                    "name": "Test Product 1",
                    "description": "Test description 1",
                    "ingredients": ["Ingredient 1", "Ingredient 2"],
                    "concerns": [["Test concern 1"]],
                    "category": ["Test Category", "Test Subcategory"],
                    "price": "100.00",
                    "product_file": None,
                    "best_seller": True,
                    "new_arrived": False
                },
                {
                    "product_id": 2,
                    "name": "Test Product 2",
                    "description": "Test description 2",
                    "ingredients": ["Ingredient 3", "Ingredient 4"],
                    "concerns": [["Test concern 2"]],
                    "category": ["Test Category 2", "Test Subcategory 2"],
                    "price": "200.00",
                    "product_file": None,
                    "best_seller": False,
                    "new_arrived": True
                }
            ]
        }
    }
    
    file_path = tmp_path / "test_products.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    
    return str(file_path)

@pytest.fixture
def invalid_json_file(tmp_path):
    """Fixture to create an invalid JSON file for testing."""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json")
    
    return str(file_path)

@pytest.fixture
def empty_json_file(tmp_path):
    """Fixture to create an empty JSON file for testing."""
    file_path = tmp_path / "empty.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({}, f)
    
    return str(file_path)

def test_successful_conversion(sample_json_file):
    """Test successful conversion of JSON to DataFrame."""
    df = convert_json_to_df(sample_json_file)
    
    # Verify the DataFrame structure and content
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    expected_columns = ['product_id', 'name', 'description', 'ingredients', 
                       'concerns', 'category', 'price', 'product_file', 
                       'best_seller', 'new_arrived']
    assert sorted(df.columns) == sorted(expected_columns)
    
    # Test specific values
    assert df.iloc[0]['product_id'] == 1
    assert df.iloc[0]['name'] == 'Test Product 1'
    assert df.iloc[0]['price'] == '100.00'
    assert df.iloc[0]['best_seller'] == True
    assert df.iloc[1]['name'] == 'Test Product 2'
    assert df.iloc[1]['new_arrived'] == True

def test_file_not_found():
    """Test handling of non-existent file."""
    with pytest.raises(FileNotFoundError) as exc_info:
        convert_json_to_df('nonexistent.json')
    assert 'JSON file not found' in str(exc_info.value)

def test_invalid_json_format(invalid_json_file):
    """Test handling of invalid JSON format."""
    with pytest.raises(ValueError) as exc_info:
        convert_json_to_df(invalid_json_file)
    assert 'Invalid JSON format' in str(exc_info.value)

def test_empty_json(empty_json_file):
    """Test handling of empty JSON file."""
    with pytest.raises(ValueError) as exc_info:
        convert_json_to_df(empty_json_file)
    assert 'JSON data must be a non-empty dictionary' in str(exc_info.value)

def test_missing_required_keys(tmp_path):
    """Test handling of JSON without required keys."""
    file_path = tmp_path / "missing_keys.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"data": {"not_products": []}}, f)
    
    with pytest.raises(ValueError) as exc_info:
        convert_json_to_df(str(file_path))
    assert 'JSON must contain' in str(exc_info.value)
