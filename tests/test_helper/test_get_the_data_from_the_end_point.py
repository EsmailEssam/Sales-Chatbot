import pytest
import json
import os
import requests
from unittest.mock import patch, Mock, mock_open
from modules.helper.get_the_data_from_the_end_point import fetch_and_save_products

@pytest.fixture
def sample_products_data():
    """Fixture providing sample product data."""
    return {
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

@pytest.fixture
def mock_successful_response(sample_products_data):
    """Fixture creating a mock successful response."""
    mock_response = Mock()
    mock_response.json.return_value = sample_products_data
    mock_response.raise_for_status.return_value = None
    return mock_response

def test_successful_fetch_and_save(tmp_path, mock_successful_response, sample_products_data):
    """Test successful API fetch and file save."""
    # Setup
    save_dir = tmp_path / "test_dataset"
    expected_file_path = save_dir / "products.json"
    
    # Mock the requests.get call
    with patch('requests.get', return_value=mock_successful_response):
        # Execute
        result = fetch_and_save_products(
            api_url="https://test-api.com/products",
            save_dir=str(save_dir)
        )
        
        # Verify
        assert result == sample_products_data
        assert expected_file_path.exists()
        
        # Verify file contents
        with open(expected_file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            assert saved_data == sample_products_data

def test_api_request_failure():
    """Test handling of API request failure."""
    # Mock a failed request
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.RequestException("API Error")
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(requests.RequestException) as exc_info:
            fetch_and_save_products(api_url="https://test-api.com/products")
        assert "API Error" in str(exc_info.value)

def test_invalid_json_response(tmp_path):
    """Test handling of invalid JSON response."""
    # Mock a response with invalid JSON
    mock_response = Mock()
    mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
    mock_response.raise_for_status.return_value = None
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(json.JSONDecodeError) as exc_info:
            fetch_and_save_products(
                api_url="https://test-api.com/products",
                save_dir=str(tmp_path)
            )
        assert "Invalid JSON" in str(exc_info.value)

def test_file_save_error(tmp_path, mock_successful_response):
    """Test handling of file save errors."""
    # Create a directory with the same name as our target file to cause an OSError
    save_dir = tmp_path / "test_dataset"
    save_dir.mkdir()
    file_path = save_dir / "products.json"
    file_path.mkdir()  # This will cause an OSError when trying to write to it
    
    with patch('requests.get', return_value=mock_successful_response):
        with pytest.raises(OSError):
            fetch_and_save_products(
                api_url="https://test-api.com/products",
                save_dir=str(save_dir)
            )

def test_default_parameters(mock_successful_response, sample_products_data):
    """Test function works with default parameters."""
    mock_open_file = mock_open()
    
    with patch('requests.get', return_value=mock_successful_response) as mock_get, \
         patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', mock_open_file):
        
        result = fetch_and_save_products()
        
        # Verify default API URL was used
        mock_get.assert_called_once_with("https://nileva.meta-bytes.net/api/products")
        
        # Verify default save directory
        mock_makedirs.assert_called_once_with("Dataset", exist_ok=True)
        
        # Verify data was returned
        assert result == sample_products_data
        
        # Verify file was opened with correct path
        mock_open_file.assert_called_once_with(
            os.path.join("Dataset", "products.json"),
            'w',
            encoding='utf-8'
        )

def test_custom_parameters(mock_successful_response, sample_products_data):
    """Test function works with custom parameters."""
    custom_url = "https://custom-api.com/products"
    custom_dir = "custom_dir"
    mock_open_file = mock_open()
    
    with patch('requests.get', return_value=mock_successful_response) as mock_get, \
         patch('os.makedirs') as mock_makedirs, \
         patch('builtins.open', mock_open_file):
        
        result = fetch_and_save_products(api_url=custom_url, save_dir=custom_dir)
        
        # Verify custom URL was used
        mock_get.assert_called_once_with(custom_url)
        
        # Verify custom save directory
        mock_makedirs.assert_called_once_with(custom_dir, exist_ok=True)
        
        # Verify data was returned
        assert result == sample_products_data
        
        # Verify file was opened with correct path
        mock_open_file.assert_called_once_with(
            os.path.join(custom_dir, "products.json"),
            'w',
            encoding='utf-8'
        ) 