from rest_framework import serializers
from .models import merchant_service_details


class MerchantServiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = merchant_service_details
        fields = '__all__'
