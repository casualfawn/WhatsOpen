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
import datetime

# Transformation and Storage Endpoint for csv file
class StoreInitialCsvView(APIView):
    parser_classes = [MultiPartParser, FormParser]

#   @api_view(['POST']) for fx based view, define post
    def post(self, request):
       # file = request.FILES['file']
        companiesdf = transform_company_df(pd.read_csv(file))
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
            serializer.save()
            print('New Restaurant Data stored successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        all_restaurant_data = TransformedCompanyData.objects.all()
        if not all_restaurant_data:
            return Response({"message": "No data available to process"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransformedCompanyDataSerializer(all_restaurant_data, many=True)
        return Response(serializer.data)