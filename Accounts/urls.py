from django.urls import path
from Accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.AccountRegisterView.as_view(), name='account_register'),
    path('login/', views.AccountLoginView.as_view(), name='account_login'),
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
