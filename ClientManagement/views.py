import json
from django.urls import reverse

from django.shortcuts import render

from rest_framework.views import APIView
from . import serializers, models
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone

from .serializers import ClientUpdateSerializer
from ClientManagement.forms import ClientUpdateForm


class ClientView(APIView):
    def post(self, request):
        data = {
            'client_name': request.data.get('client-name'),
            'client_number': request.data.get('client-number'),
            'client_address': request.data.get('client-address'),
            'active_plan': request.data.get('active-plan'),
            'plan_start_date': request.data.get('plan-start-date'),
            'plan_end_date': request.data.get('plan-end-date'),
            'total_amount': int(request.data.get('total-amount')),
            'amount_paid': int(request.data.get('amount-paid')),
            'account': 1
        }
        serializer = serializers.ClientSaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            redirect_url = '/accounts/dashboard/'
            return JsonResponse(data={'message': 'Client saved successful', 'redirect_url': redirect_url},
                                status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(data={'message': f'Client failed with {serializer.error_messages}'},
                                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return render(request, 'add_client.html')

    def put(self, request):
        try:
            data = {
                'client_name': request.data.get('client_name'),
                'client_number': request.data.get('client_number'),
                'client_address': request.data.get('client_address'),
                'active_plan': request.data.get('active_plan'),
                'plan_start_date': request.data.get('plan_start_date'),
                'plan_end_date': request.data.get('plan_end_date'),
                'total_amount': int(request.data.get('total_amount')),
                'amount_paid': int(request.data.get('amount_paid')),
                'account': 1
            }
            client = models.Client.objects.get(pk=request.data.get('client_id'))
            serializer = serializers.ClientSaveSerializer(client, data=data)
            if serializer.is_valid():
                serializer.save()
                redirect_url = '/accounts/dashboard/'
                return JsonResponse(
                    data={'message': f'Client {serializer.data["client_name"]} updated', 'redirect_url': redirect_url},
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


class ClientsListView(APIView):
    def get(self, request):
        try:
            clients = models.Client.objects.all()
            serializer = serializers.ClientGetSerializer(clients, many=True)
            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK, safe=False)
        except Exception as e:
            return JsonResponse(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteClientsView(APIView):
    def get(self, request):
        return render(request, 'delete_clients.html')

    def delete(self, request):
        try:
            client_ids = request.data.get('client_ids', [])
            if not isinstance(client_ids, list):
                raise ValueError("Client IDs must be provided as a list")

            clients = models.Client.objects.filter(client_id__in=client_ids)
            for client in clients:
                client.is_active = False
                client.save()
            dashboard_url = reverse('accounts:dashboard')
            return JsonResponse({'message': 'Clients deleted successfully', 'redirect_url': dashboard_url},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message': f'Failed to delete clients due to {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateClientsView(APIView):
    def get(self, request):
        return render(request, 'all_clients.html')

    def post(self, request):
        client_id = int(request.data.get('client_id'))
        client = models.Client.objects.get(client_id=client_id)
        form = ClientUpdateForm(instance=client)  # Pre-fill the form with the client data
        return render(request, 'update_client_form.html', {'form': form})


class GetClientView(APIView):
    def get(self, request, client_id):
        try:
            client = models.Client.objects.get(client_id=client_id)
            serializer = ClientUpdateSerializer(client, many=False)
            return JsonResponse({'message': 'Details of selected client', 'data': serializer.data},
                                status=status.HTTP_200_OK, safe=False)
        except models.Client.DoesNotExist:
            return JsonResponse({'message': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
