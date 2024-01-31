import json
import os
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.views import View
from database.models import User
from common import password_policy
from django.shortcuts import render

class LoginHandler(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        response = {'success': False}

        if not email or not password:
            response['message'] = 'Email and password are required'
            return JsonResponse(response)

        user = User.objects.filter(email=email, password=password).first()
        if not user:
            response['message'] = 'Email or password is incorrect'
            return JsonResponse(response)
        
        response['success'] = True
        response['message'] = 'User logged in successfully'
        response = JsonResponse(response)
        response.set_cookie('user_mail', email)
        return response
    
class RegisterHandler(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        password_validate = data.get('passwordValidate')
        response = {'success': False}

        if not password_policy(password, password_validate):
            response['message'] = 'Something went wrong with your password'
            return JsonResponse(response)

        if not name or not email or not password:
            response['message'] = 'Name, email and password are required'
            return JsonResponse(response)

        user = User.objects.filter(email=email).first()

        if user:
            response['message'] = 'User already exists'
            return JsonResponse(response)

        user = User.objects.create(name=name, email=email, password=password)
        response['success'] = True
        response['message'] = 'User created successfully'
        return JsonResponse(response)

def loginPage(request):
    return render(request, 'login/sign-in.html')

def register(request):
    return render(request, 'login/sign-up.html')