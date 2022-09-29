import os
import json
import requests
from rest_framework import status
from dotenv import load_dotenv

load_dotenv()

# Create your tests here.
class TestVcfDataRow:
    def test_create_new_data_row(self):
        domain = os.environ.get('APP_DOMAIN')
        url = '/'.join([domain, 'api/data/row'])
        
        payload = {
            "ID": "rs1",
            "CHROM": "chr10",
            "POS": 1000,
            "ALT": "A",
            "REF": "G"
        }

        response = requests.post(url, data=payload)
        
        assert response.status_code \
            == status.HTTP_403_FORBIDDEN
        
        
        headers = {
            'Authorization': 'somesecretkey'
        }

        response = requests.post(
            url, data=json.dumps(payload), headers=headers
        )
        results = response.json()
        
        assert response.status_code \
            == status.HTTP_201_CREATED
        assert payload == results


        payload = {
            "CHROM": "chr10",
            "POS": 1000,
            "ALT": "A",
            "REF": "G"
        }

        response = requests.post(
            url, data=json.dumps(payload), headers=headers
        )
        results = response.json()

        assert response.status_code \
            == status.HTTP_400_BAD_REQUEST
        assert results['ID']
        assert len(results['ID']) == 1

    
    def test_update_existing_data_row(self):
        domain = os.environ.get('APP_DOMAIN')
        url = '/'.join([domain, 'api/data/row'])
        
        payload = {
            "ID": "rs1",
            "CHROM": "chr10",
            "POS": 1000,
            "ALT": "A",
            "REF": "G"
        }

        response = requests.put(url, data=payload)
        
        assert response.status_code \
            == status.HTTP_403_FORBIDDEN
        
        
        headers = {
            'Authorization': 
                os.environ.get('AUTH_SECRET_KEY')
        }

        response = requests.put(
            url, data=json.dumps(payload), headers=headers
        )
        results = response.json()
        
        assert response.status_code \
            == status.HTTP_400_BAD_REQUEST

        response = requests.put(
            url, 
            params={'id': 'rs1'},
            data=json.dumps(payload), 
            headers=headers
        )
        results = response.json()
        
        assert response.status_code \
            == status.HTTP_200_OK
        assert payload == results


        payload = {
            "CHROM": "chr10",
            "POS": 1000,
            "ALT": "A",
            "REF": "G"
        }

        response = requests.put(
            url, 
            params={'id': 'rs1'},
            data=json.dumps(payload), 
            headers=headers
        )
        results = response.json()

        assert response.status_code \
            == status.HTTP_400_BAD_REQUEST
        assert results['ID']
        assert len(results['ID']) == 1


    def test_delete_existing_data_row(self):
        domain = os.environ.get('APP_DOMAIN')
        url = '/'.join([domain, 'api/data/row'])

        response = requests.delete(url)
        
        assert response.status_code \
            == status.HTTP_403_FORBIDDEN
        
        
        headers = {
            'Authorization': 'somesecretkey'
        }

        response = requests.put(
            url, headers=headers
        )
        
        assert response.status_code \
            == status.HTTP_400_BAD_REQUEST

        response = requests.delete(
            url, 
            params={'id': 'rs1'}, 
            headers=headers
        )
        
        assert response.status_code \
            == status.HTTP_204_NO_CONTENT
