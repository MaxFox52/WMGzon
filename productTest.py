import json
import pytest
from unittest.mock import mock_open, patch
from jsonmanager import ProductManager

# Sample product dictionary for testing
sample_product = {"id": 1, "product_name": "Product", "storage_sizes": [128, 256, 512, 1], "colours": ["Red", "Blue"], "description": "Description", "imageid": "image.png", "product_type": "phone", "price": "949", "sellerid": "seller", "rating": 5}
another_product = {"id": 2, "product_name": "Product2", "storage_sizes": [256, 512], "colours": ["Red"], "description": "Description", "imageid": "image.png", "product_type": "phone", "price": "949", "sellerid": "seller", "rating": 5}

def test_load_data():
    with patch('builtins.open', mock_open(read_data=json.dumps([sample_product]))) as mocked_file:
        with patch('json.load', return_value=[sample_product]):
            manager = ProductManager()
            assert manager.getProducts() == [sample_product]
            mocked_file.assert_called_once_with(ProductManager.JSON_FILE)

def test_save_data():
    with patch('builtins.open', mock_open()) as mocked_file:
        with patch('json.dump') as mocked_json_dump:
            manager = ProductManager()
            manager.saveData([sample_product])
            mocked_file.assert_called_once_with(ProductManager.JSON_FILE, 'w')
            mocked_json_dump.assert_called_once_with([sample_product], mocked_file())

def test_insert_product():
    with patch('builtins.open', mock_open()) as mocked_file:
        with patch('json.dump'), patch('json.load', return_value=[sample_product]):
            manager = ProductManager()
            manager.insertProduct(another_product)
            assert manager.getProducts()[0]['id'] == sample_product['id'] + 1
            assert manager.getProducts()[0] == another_product.toDic()

def test_update_product():
    updated_product = {"id": 1, "product_name": "Product", "storage_sizes": [128, 256, 512, 1], "colours": ["Red", "Blue"], "description": "Description", "imageid": "image.png", "product_type": "phone", "price": "120", "sellerid": "seller", "rating": 5}
    with patch('builtins.open', mock_open()) as mocked_file:
        with patch('json.dump'), patch('json.load', return_value=[sample_product]):
            manager = ProductManager()
            manager.updateProduct(1, updated_product)
            assert manager.getProducts()[0] == updated_product.toDic()

def test_delete_product():
    with patch('builtins.open', mock_open()) as mocked_file:
        with patch('json.dump'), patch('json.load', return_value=[sample_product, another_product]):
            manager = ProductManager()
            manager.deleteProduct(1)
            assert sample_product not in manager.getProducts()

def test_get_products():
    with patch('builtins.open', mock_open(read_data=json.dumps([sample_product]))):
        with patch('json.load', return_value=[sample_product]):
            manager = ProductManager()
            assert manager.getProducts() == [sample_product]

def test_get_product():
    with patch('builtins.open', mock_open()) as mocked_file:
        with patch('json.dump'), patch('json.load', return_value=[sample_product, another_product]):
            manager = ProductManager()
            product = manager.getProduct(2)
            assert product == another_product


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))