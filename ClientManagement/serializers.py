from rest_framework import serializers
from ClientManagement.models import Client


class ClientSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = ['client_id']


class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name', 'client_number', 'client_address', 'client_image', 'client_date_of_joined',
                  'active_plan', 'plan_start_date', 'plan_end_date', 'total_amount', 'amount_paid']


class ClientGetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['client_name', 'client_id']
