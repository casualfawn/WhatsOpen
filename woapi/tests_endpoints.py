
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from .models import TransformedCompanyData

class TestStoreSingleEntryApiTest(ApiTestCase):
    def tests_setup(self):
        self.companies_data = {
            'company_name':'Restaurant A',
            'open':'12:00:00',
            'close':'14:00:00',
            'wkday':'Mon'
        }
        self.company_name = TransformedCompanyData.objects.create(**self.company_name)
        self.open = TransformedCompanyData.objects.create(**self.open)
        self.close = TransformedCompanyData.objects.create(**self.close)
        self.wkday = TransformedCompanyData.objects.create(**self.wkday)
        self.url = '/woapi/storesingleentry/'

    def tests_add_new_company_data_single_entry(self):
        response = self.client.post(self.url, self.company_data, format='json')
        self.assertEqual(response.data['company_name'], self.company_data['company_name'])
        self.assertEqual(response.data['open'], self.company_data['open'])
        self.assertEqual(response.data['close'], self.company_data['close'])
        self.assertEqual(response.data['wkday'], self.company_data['wkday'])


    # write a test to test the entries that have the new binned 00:00:00 to close time.


