import os
from dotenv import load_dotenv
import pytest
import requests
from django.urls import reverse
from rest_framework import status

load_dotenv()

# Create your tests here.
class TestVcfDataList:
    def test_get_data_list(self):
        domain = os.environ.get('APP_DOMAIN')
        url = '/'.join([domain, 'api/data/list'])
        
        headers = {'Accept': '*/*'}
        response = requests.get(url, headers=headers)
        results = response.json()
        
        assert response.status_code == status.HTTP_200_OK
        assert results['count'] > 0
        assert 'application/json' in response.headers[
            'Content-Type'
        ]


        headers = {'Accept': 'application/xml'}
        response = requests.get(url, headers=headers)

        assert 'application/xml' in response.headers[
            'Content-Type'
        ]
        

        headers = {'Accept': 'wrong/header'}
        response = requests.get(url, headers=headers)
        
        assert response.status_code \
            == status.HTTP_406_NOT_ACCEPTABLE


        params = {'id': 'b@dvalu3#'}
        response = requests.get(url, params=params)
        
        assert response.status_code \
            == status.HTTP_400_BAD_REQUEST
