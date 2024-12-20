from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from .models import TransformedCompanyData
from .serializers import TransformedCompanyDataSerializer
from woapi.utils.utils import *
import pandas as pd
import os
from datetime import datetime

# Transformation and Storage Endpoint for csv file
class StoreInitialCsvView(APIView):
    parser_classes = [MultiPartParser, FormParser]
#   @api_view(['POST']) for fx based view, define post
    def post(self, request):
       # file = request.FILES['file']
        filepath_loc = os.path.join(os.path.expanduser("~/"), "comps.csv")
        companiesdf = transform_company_df(pd.read_csv(filepath_loc))
        for i, j in companiesdf.iterrows():
            companies_data = {
                'wkday':j['wkday'],
                'company_name':j['company_name'],
                'open':j['open'],
                'close':j['close']
            }
            serializer = TransformedCompanyDataSerializer(data=companies_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response('Serliazer invalid, CSV Data not uploaded', status = 400)
        return Response('Initial CSV Uploaded', status=201)


# Transformation and Storage Endpoint
class StoreSingleEntryView(APIView):
# Transform functions in utils.py
    def post(self, request, *args, **kwargs):
        serializer = TransformedCompanyDataSerializer(data = request.data)
        if serializer.is_valid():
            if len(request.data) == 4:
                serializer.save()
                print('New Restaurant Data stored successfully')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Invalid Data Provided')
            return Response({"No data provided"}, status=status.HTTP_400_BAD_REQUEST)


# Endpoint to get all companies data
class GetAllView(APIView):
    def get(self, request, *args, **kwargs):
        all_restaurant_data = TransformedCompanyData.objects.all()
        if not all_restaurant_data:
            return Response({"message": "No data available to process"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransformedCompanyDataSerializer(all_restaurant_data, many=True)
        return Response(serializer.data)

# Endpoint to get company data based on date time string input
class GetOpenCompaniesView(APIView):
    def get(self, request, *args, **kwargs):
        input_date = request.query_params.get('date', None)
        if not input_date:
            return Response({"No date was provided."}, status=status.HTTP_400_BAD_REQUEST)
        input_date = datetime.strptime(input_date, '%Y-%m-%dT%H:%M:%S')
        input_date_wkday = input_date.strftime('%a')
        input_date_time = input_date.time()
        open_companies = TransformedCompanyData.objects.filter(wkday = input_date_wkday,open__lt=input_date_time, close__gt=input_date_time)
        serializer = TransformedCompanyDataSerializer(open_companies, many = True)

        if not open_companies:
            return Response({"Data incorrectly provided"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

