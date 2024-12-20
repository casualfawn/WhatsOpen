
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from datetime import time
from .models import TransformedCompanyData
from . import views


class TestStoreSingleEntryApiTest(APITestCase):

    def test_store_new_company_record(self):
        company_data = {
            'company_name':'Restaurant A',
            'open':'12:00:00',
            'close':'14:00:00',
            'wkday':'Mon'
        }
        response = self.client.post('/woapi/storesingleentry/', company_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['company_name'], company_data['company_name'])

    def test_invalid_company_record(self):
        company_data = {
        'company_name': 'Restaurant A',
        'open': '12:00:00',
        'close': '14:00:00',
    }
        print(len(company_data))
        response = self.client.post('/woapi/storesingleentry/', company_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestGetOpenCompanies(APITestCase):

    def test_open_companies_0015(self):
        date_input = '2022-01-01T00:15:00'
        url = reverse('getcompanyavailability') + f'?date={date_input}'
        response = self.client.get(url)
       # self.assertEqual(response.status_code, status.HTTP_200_OK)
        company_test = TransformedCompanyData.objects.create(
            company_name='The Cheesecake Factory',
            open=time(00, 0),  # Opens at 9:00 AM
            close=time(00, 30),
            wkday="Sat")
        company_names = [company for company in response.data]
        self.assertIn(company_test.company_name, company_names)

    def test_open_companes_invalid_date_provided(self):
        date_input = '2022-01-01T04:1:00'
        url = reverse('getcompanyavailability') + f'?date={date_input}'
        response = self.client.get(url)
       # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(company_test.company_name, company_names)

    def test_open_companies_0305(self):
        date_input = '2022-01-01T00:15:00'
        url = reverse('getcompanyavailability') + f'?date={date_input}'
        response = self.client.get(url)
       # self.assertEqual(response.status_code, status.HTTP_200_OK)
        company_test = TransformedCompanyData.objects.create(
            company_name='The Cheesecake Factory',
            open=time(00, 0),  # Opens at 9:00 AM
            close=time(4, 30),
            wkday="Sat")
        company_names = [company for company in response.data]
        self.assertIn(company_test.company_name, company_names)

