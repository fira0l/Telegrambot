import requests
import json

# Test the API endpoint
try:
    print("Testing API endpoint...")
    response = requests.get('https://graphicdesign.onrender.com/api/images?page=1&per_page=6')
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print(f"Number of images: {len(data.get('images', []))}")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")