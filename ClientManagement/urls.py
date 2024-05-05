from django.urls import path
from ClientManagement import views

app_name = 'clients'
urlpatterns = [
    path('client/', views.ClientView.as_view(), name='client'),
    path('clients_list/', views.ClientsListView.as_view(), name='clients_list'),
    path('delete/', views.DeleteClientsView.as_view(), name='delete_clients'),
    path('update/', views.UpdateClientsView.as_view(), name='update_client'),
    path('client/<int:client_id>/', views.GetClientView.as_view(), name='get_client')
]
