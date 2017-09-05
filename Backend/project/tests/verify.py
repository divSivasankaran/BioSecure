import requests
import os
import json

with open(os.path.join('test_3.jpg'), 'rb') as fp:
    response = requests.put('http://localhost:5000/biosecure/api/v1/verify', files={'image': fp})
    print(response.text)