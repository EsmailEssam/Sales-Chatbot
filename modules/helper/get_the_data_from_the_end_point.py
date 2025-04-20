import requests
import json
import os 

# Define the API endpoint URL
api_url = "https://nileva.meta-bytes.net/api/products"

# Make GET request to the endpoint
response = requests.get(api_url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    products_data = response.json()
    
    # Save data to file for later use
    
    file_save_path = os.path.join(  "Dataset" , 'products.json')
    print(file_save_path)
    with open(file_save_path , 'w' , encoding='utf-8') as f:
        json.dump(products_data, f, indent=4)
        
    print(f"Successfully retrieved {len(products_data)} products")
    print("Data saved to products.json")
else:
    print(f"Failed to get data: {response.status_code}")
    print(response.text)
