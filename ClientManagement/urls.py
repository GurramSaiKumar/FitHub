from django.urls import path
from ClientManagement import views

urlpatterns = [
    path('client/', views.ClientView.as_view(), name='client'),
    # path('add_client/')
]
