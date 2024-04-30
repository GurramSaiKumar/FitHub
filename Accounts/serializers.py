from rest_framework import serializers
from Accounts import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['username', 'email', 'password', 'company_name', 'company_address']
        extra_kwargs = {'password': {'write_only': True}}


class AccountLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.Account
        fields = ['email', 'password']
