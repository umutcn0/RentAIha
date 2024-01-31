import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from database.models import IHA, Rent, User
from drf_yasg.utils import swagger_auto_schema

class RentOperations(View):
    # Get rent history.
    def get(self, request):
        rent_data = Rent.objects.filter(is_active=True).values()
        rent_json_data = list()
    
        for rent in rent_data:
            user = User.objects.get(pk=rent.get('user_id_id'))
            iha = IHA.objects.get(pk=rent.get('iha_id_id'))
            
            rent_json_data.append({
                "start_date": rent.get('start_date'),
                "end_date": rent.get('end_date'),
                "user_id": user.name,
                "iha_id": iha.brand + " " + iha.model,
                "id": rent.get('id'),
                })
        return JsonResponse(rent_json_data, safe=False)

    # Rent an IHA.
    def post(self, request):
        data = json.loads(request.body)
        selected_rent_id = data.get('selected_rent_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        user_mail = request.COOKIES.get('user_mail')
        response = {'success': False}

        print(selected_rent_id)
        print(start_date)
        print(end_date)
        if not selected_rent_id or not start_date or not end_date:
            response['message'] = 'IHA, start date, end date and user id are required'
            return JsonResponse(response)
        
        # Kullanıcı oluşturun veya mevcut bir kullanıcıyı seçin
        user_instance = User.objects.filter(email=user_mail).first() # Burada 1, kullanıcının id'sini temsil eder

        # IHA oluşturun veya mevcut bir IHA'yı seçin
        iha_instance = IHA.objects.filter(pk=selected_rent_id).first()

        if iha_instance and not iha_instance.is_rented and user_instance:
            iha_instance.is_rented = True
            Rent.objects.create(user_id=user_instance, iha_id=iha_instance, start_date=start_date, end_date=end_date)
            iha_instance.save()
            response['success'] = True
            response['message'] = 'IHA rented successfully'
            return JsonResponse(response)
        elif iha_instance and iha_instance.is_rented:
            response['message'] = 'IHA is already rented'
            return JsonResponse(response)
        else:
            response['message'] = 'IHA or user not found'
            return JsonResponse(response)
    
    # Update an IHA's rent information.
    def put(self, request):
        data = json.loads(request.body)
        start_date = data.get('start_date') if data.get('start_date') else None
        end_date = data.get('end_date') if data.get('end_date') else None
        selected_rent_id = data.get('selected_rent_id')
        response = {'success': False}

        print(start_date, end_date, selected_rent_id)

        if not selected_rent_id:
            response['message'] = 'Rent id is required'
            return JsonResponse(response)
        
        rent = Rent.objects.filter(pk=selected_rent_id).first()

        if rent:
            rent.start_date = start_date if start_date else rent.start_date
            rent.end_date = end_date if end_date else rent.end_date
            rent.save()
            response['success'] = True
            response['message'] = 'Rent updated successfully'
            return JsonResponse(response)
        else:
            response['message'] = 'Renting option not found'
            return JsonResponse(response)
    
    # Delete an IHA's rent information.
    def delete(self, request):
        data = json.loads(request.body)
        selected_rent_id = data.get('selected_rent_id')
        response = {'success': False}

        if not selected_rent_id:
            response['message'] = 'User id and IHA id are required'
            return JsonResponse(response)
        
        rent = Rent.objects.filter(pk=selected_rent_id).first()
        iha = IHA.objects.filter(pk=rent.iha_id_id).first()

        if rent:
            iha.is_rented = False
            iha.save()
            rent.delete()
            response['success'] = True
            response['message'] = 'Rent deleted successfully'
            return JsonResponse(response)
        else:
            response['message'] = 'Renting option not found'
            return JsonResponse(response)
        
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def history(request):
    return render(request, 'dashboard/history.html')