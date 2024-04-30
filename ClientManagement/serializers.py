from rest_framework import serializers
from ClientManagement import models


class ClientSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class ClientGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['client_name', 'client_number', 'client_address', 'client_image', 'client_date_of_joined',
                  'active_plan', 'plan_start_date', 'plan_end_date', 'total_amount', 'amount_paid']


class ClientGetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['client_name', 'client_id']
