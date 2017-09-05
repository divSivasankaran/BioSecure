import requests
import os
import json

with open(os.path.join('test_2.jpg'), 'rb') as fp:
    # file = FileStorage(fp)
    response = requests.put('http://localhost:5000/biosecure/api/v1/enroll', files={'image': fp})
    print(response)