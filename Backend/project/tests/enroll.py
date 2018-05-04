import requests
import os
import json

with open(os.path.join('obama1.jpg'), 'rb') as fp:
    # file = FileStorage(fp)
    response = requests.post('http://localhost:5000/biosecure/api/v1/enroll', files={'image': fp})
    print(response)