from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TransformedCompanyData
from .serializers import TransformedCompanyDataSerializer
import datetime

# Transformation and Storage Endpoint
class StoreView(APIView):
# Transform functions will be in utils.py
    def post(self, request, *args, **kwargs):
        companydata = request.data.get('data')
        if not companydata:
            return Response({"No data provided"}, status=status.HTTP_400_BAD_REQUEST)

        transformed_data = TransformedCompanyData.objects.create(data=companydata)
        return Response({
            "message": "Restaurant data has been stored successfully",
            "id": transformed_data.id,
            "data": transformed_data.data
        }, status=status.HTTP_201_CREATED)

# Endpoint to pull data based on date time string input
class DataView(APIView):
    def get(self, request, *args, **kwargs):
        all_restaurant_data = TransformedCompanyData.objects.all()
        if not all_restaurant_data:
            return Response({"message": "No data available to process"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransformedCompanyDataSerializer(all_restaurant_data, many=True)
        return Response(serializer.data)