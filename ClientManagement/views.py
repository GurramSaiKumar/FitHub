from django.shortcuts import render

from rest_framework.views import APIView
from . import serializers, models
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone


class ClientView(APIView):
    def post(self, request):
        client_data = request.data
        serializer = serializers.ClientSaveSerializer(client_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data={'message': 'Client saved successful'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(data={'message': f'Client failed with {serializer.error_messages}'},
                                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            clients = models.Client.objects.all()
            serializer = serializers.ClientGetSerializer(clients, many=True)
            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            data = request.data
            client = models.Client.objects.get(pk=data['id'])
            serializer = serializers.ClientSaveSerializer(client, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(data={'message': f'Client {serializer.data["client_name"]} updated'},
                                    status=status.HTTP_200_OK)
            return JsonResponse(data={'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except models.Client.DoesNotExist:
            return JsonResponse(data={'message': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            data = request.data
            client = models.Client.objects.get(pk=data['id'])
            client.delete()
            return JsonResponse(data={'message': f'Client {client.client_name} has been deleted'},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientAttendanceView(APIView):
    def post(self, request):
        try:
            client_ids = [data['client_id'] for data in request.data]
            clients = models.Client.objects.filter(client_id__in=client_ids)
            attendances = [models.Attendance(client=client) for client in clients]
            models.Attendance.objects.bulk_create(attendances)
            return JsonResponse(data={'message': 'Attendance saved'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={'message': {str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            today = timezone.now().date()
            clients_with_attendance = (models.Attendance.objects.filter(attendance_date=today).
                                       select_related('client_id', 'client_name'))
            clients_without_attendance = (models.Attendance.objects.exclude(attendance_date=today).
                                          select_related('client_id', 'client_name'))
            clients_with_attendance = serializers.ClientGetAttendanceSerializer(data=clients_with_attendance, many=True)
            clients_without_attendance = serializers.ClientGetAttendanceSerializer(data=clients_without_attendance,
                                                                                   many=True)
            return JsonResponse(data={'message': {'clients_with_attendance': clients_with_attendance,
                                                  'clients_without_attendance': clients_without_attendance}},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse(data={str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)