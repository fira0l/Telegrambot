import requests
import json

# Test the API endpoint
try:
    response = requests.get('http://localhost:5000/api/images?page=1&per_page=6')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")