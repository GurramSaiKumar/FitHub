from rest_framework.views import APIView
from Accounts import serializers
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.urls import reverse
from django.shortcuts import render
from Accounts.models import Account
from django.shortcuts import redirect, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required


class AccountRegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        account_data = request.data
        serializer = serializers.AccountSerializer(data=account_data)
        if serializer.is_valid():
            serializer.save()
            login_url = reverse('account_login')
            # Construct the message with the login URL
            message = format_html('Account registered successfully. Please <a href="{}">login</a> to continue.',
                                  login_url)
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class AccountLoginView(APIView):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = serializers.AccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_ = serializer.validated_data['email']
            password_ = serializer.validated_data['password']
            account = Account.objects.filter(email=email_, password=password_)
            if account:
                redirect_url = '/accounts/dashboard/'
                return JsonResponse({'success': True, 'redirect_url': redirect_url})
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LandingPageView(APIView):
    def get(self, request):
        return render(request, 'landingpage.html')


class DashboardView(APIView):
    def get(self, request):
        return render(request, 'dashboard.html')
