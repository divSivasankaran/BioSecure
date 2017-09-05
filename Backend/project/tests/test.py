
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 16:51:06 2017

@author: divya
"""

import unittest
import requests    
import json 
from project import app
 
 
class ProjectTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base = 'http://localhost:5000/biosecure/api/v1/'
 
        self.assertEquals(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
    ########################
    #### helper methods ####
    ########################
 
 
 
    ###############
    #### tests ####
    ###############
 
def test_recipes_api_sending_file(self):
    headers = self.get_headers_authenticated_admin()
    with open(os.path.join('project', 'tests', 'image.jpg'), 'rb') as fp:
        response = self.app.put('http://localhost:5000/biosecure/api/v1/enroll', data={'image': fp}, headers=headers,
                                content_type='multipart/form-data', follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))
        print(json_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('True', json_data['result'])

 
 
if __name__ == "__main__":
    unittest.main()





