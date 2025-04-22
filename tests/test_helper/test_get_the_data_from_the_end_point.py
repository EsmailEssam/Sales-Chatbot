import pytest
import json
import os
from unittest.mock import patch, MagicMock
from modules.helper.get_the_data_from_the_end_point import ProductDataFetcher


# ✅ اختبار: fetch_data بيجيب بيانات صحيحة
@patch("modules.helper.get_the_data_from_the_end_point.requests.get")
def test_fetch_data_success(mock_get):
    mock_response = MagicMock()
    expected_data = {"products": [{"id": 1, "name": "Product 1"}]}
    mock_response.json.return_value = expected_data
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    fetcher = ProductDataFetcher()
    data = fetcher.fetch_data()

    assert data == expected_data
    mock_get.assert_called_once_with(fetcher.api_url)


# ✅ اختبار: fetch_data بيرفع Exception لو الـ API واقع
@patch("modules.helper.get_the_data_from_the_end_point.requests.get")
def test_fetch_data_failure(mock_get):
    mock_get.side_effect = Exception("API is down")

    fetcher = ProductDataFetcher()

    with pytest.raises(Exception) as exc_info:
        fetcher.fetch_data()

    assert "API is down" in str(exc_info.value)


# ✅ اختبار: save_data بيكتب ملف JSON في المكان المطلوب
def test_save_data_creates_file(tmp_path):
    fetcher = ProductDataFetcher(save_dir=str(tmp_path))
    sample_data = {"products": [{"id": 1, "name": "Test"}]}

    saved_path = fetcher.save_data(sample_data)

    assert os.path.exists(saved_path)

    with open(saved_path, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)

    assert loaded_data == sample_data


# ✅ اختبار: run بيشغل fetch و save و يرجع البيانات
@patch.object(ProductDataFetcher, "fetch_data")
@patch.object(ProductDataFetcher, "save_data")
def test_run_success(mock_save, mock_fetch):
    fake_data = {"products": [{"id": 42, "name": "Fake"}]}
    mock_fetch.return_value = fake_data

    fetcher = ProductDataFetcher()
    result = fetcher.run()

    assert result == fake_data
    mock_fetch.assert_called_once()
    mock_save.assert_called_once_with(fake_data)


# ✅ اختبار: run بيرفع error لو حصل exception في fetch_data
@patch.object(ProductDataFetcher, "fetch_data")
def test_run_raises_exception_on_fetch_error(mock_fetch):
    mock_fetch.side_effect = Exception("Fetch failed")

    fetcher = ProductDataFetcher()

    with pytest.raises(Exception) as exc_info:
        fetcher.run()

    assert "Fetch failed" in str(exc_info.value)
