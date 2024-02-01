import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from database.models import IHA

class IhaHandler(View):
    # Get all IHAs.
    def get(self, request):
        iha_data = IHA.objects.filter(is_active=True).values()
        iha_json_data = list()
        for iha in iha_data:
            iha_json_data.append({
                "Brand": iha.get('brand'),
                "Model": iha.get('model'),
                "Weight": iha.get('weight'),
                "Category": iha.get('category'),
                "Year": iha.get('year'),
                "Price": iha.get('price'),
                "is_rented": iha.get('is_rented'),
                "id": iha.get('id'),
                })
        return JsonResponse(iha_json_data, safe=False)
    
    # Create an IHA.
    def post(self, request):
        data = json.loads(request.body)
        brand = data.get('brand')
        model = data.get('model')
        weight = data.get('weight')
        category = data.get('category')
        year = data.get('year')
        price = data.get('price')
        response = {'success': False}

        if not brand or not model or not weight or not category or not year or not price:
            response['message'] = 'Brand, model, weight, category, year and price are required'
            return JsonResponse(response)
        
        IHA.objects.create(brand=brand, model=model, weight=weight, category=category, year=year, price=price)
        response['success'] = True
        response['message'] = 'IHA created successfully'
        return JsonResponse(response)

    # Update an IHA's information.
    def put(self, request):
        data = json.loads(request.body)
        brand = data.get('brand')
        model = data.get('model')
        weight = data.get('weight')
        category = data.get('category')
        year = data.get('year')
        price = data.get('price')
        selected_iha_id = data.get('selected_iha_id')
        response = {'success': False}

        if not brand or not model or not weight or not category or not year or not price or not selected_iha_id:
            response['message'] = 'Brand, model, weight, category, year, price and selected_iha_id are required'
            return JsonResponse(response)
        
        iha_instance = IHA.objects.filter(pk=selected_iha_id).first()
        if iha_instance and iha_instance.brand == brand and iha_instance.model == model:
            iha_instance.brand = brand if brand else iha_instance.brand
            iha_instance.model = model if model else iha_instance.model
            iha_instance.weight = weight if weight else iha_instance.weight
            iha_instance.category = category if category else iha_instance.category
            iha_instance.year = year if year else iha_instance.year
            iha_instance.price = price if price else iha_instance.price
            iha_instance.save()
            response['success'] = True
            response['message'] = 'IHA updated successfully'
            return JsonResponse(response)
        else:
            response['message'] = 'IHA not found'
            return JsonResponse(response)
    
    # Delete an IHA.
    def delete(self, request):
        data = json.loads(request.body)
        selected_iha_id = data.get('selected_iha_id')
        response = {'success': False}

        if not selected_iha_id:
            response['message'] = 'IHA id is required'
            return JsonResponse(response)
        
        iha_instance = IHA.objects.filter(pk=selected_iha_id).first()
        if iha_instance:
            iha_instance.delete()
            response['success'] = True
            response['message'] = 'IHA deleted successfully'
            return JsonResponse(response)
        else:
            response['message'] = 'IHA not found'
            return JsonResponse(response)

# Render the IHA page.
def iha(request):
    return render(request, 'dashboard/iha.html')
