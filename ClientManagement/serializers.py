from rest_framework import serializers
from ClientManagement.models import Client
from django import forms


class ClientSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['client_id']


class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['client_id', 'account']


class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_id', 'client_name', 'client_number']


class ClientGetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name', 'client_id']



