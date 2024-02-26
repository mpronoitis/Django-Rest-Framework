import requests
product_id = int(input("What is the product id that you want to delete"))
endpoint = f"http://localhost:8000/api/products/{product_id}/delete"
get_response = requests.delete(endpoint) 
print(get_response.status_code)