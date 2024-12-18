
from rest_framework import serializers
from .models import TransformedCompanyData

class TransformedCompanyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformedCompanyData
        fields = ['id', 'company_name', 'open', 'close', 'day']