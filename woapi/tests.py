
from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from datetime import time
import pandas as pd
import os
from .models import TransformedCompanyData
from .serializers import TransformedCompanyDataSerializer
from . import views
from .utils.utils import transform_company_df

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
    # The datetime we want to check (e.g., 10:30 AM on Dec 20, 2024)


    def test_open_companies_0015(self):
        input_date = '2022-01-01T00:15:00'
        input_date = datetime.strptime(input_date, '%Y-%m-%dT%H:%M:%S')
        input_date_wkday = input_date.strftime('%a')
        input_date_time = input_date.time()
        filepath_loc = os.path.join(os.path.expanduser("~/"), "comps.csv")
        companiesdf = transform_company_df(pd.read_csv(filepath_loc))
        companies_data = {
                'wkday': j['Sat'],
                'company_name': j['The Cheesecake Factory'],
                'open': j['open'],
                'close': j['close']
            }
        serializer = TransformedCompanyDataSerializer(data = companies_data, many = True)
        if serializer.is_valid():
            serializer.save()
        open_companies = TransformedCompanyData.objects.filter(wkday = input_date_wkday,open__lt=input_date_time, close__gt=input_date_time)
        serializer = TransformedCompanyDataSerializer(data = open_companies)
        if serializer.is_valid():

            print(serializer.data)
            print(open_companies)
            Response(serializer.data, status=status.HTTP_201_CREATED)
       # self.assertIn(company_test.company_name, company_names)

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

