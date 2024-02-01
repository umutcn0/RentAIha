import json
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from database.models import IHA  # IHA modelini içe aktardığınızdan emin olun
from iha.views import IhaHandler

class IhaHandlerTest(TestCase):
    def test_get_all_ihas(self):
        # Tüm IHAs'ları almak için başarılı senaryo
        url = reverse('handler')  # 'get_all_ihas' endpoint'inizin doğru adını kullanmalısınız

        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response)
        self.assertIsInstance(json_response, list)
        self.assertEqual(len(json_response), 0)  # Test veritabanında IHA olmadığı varsayılarak 0 olarak kontrol edilmiştir.

    def test_create_iha_success(self):
        # IHA oluşturma işlemi için başarılı senaryo
        url = reverse('create_iha')  # 'create_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'brand': 'TestBrand',
            'model': 'TestModel',
            'weight': 100,
            'category': 'TestCategory',
            'year': 2023,
            'price': 2000,
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA created successfully')

        # Oluşturulan IHA'yı kontrol et
        iha = IHA.objects.first()
        self.assertIsNotNone(iha)
        self.assertEqual(iha.brand, data['brand'])
        self.assertEqual(iha.model, data['model'])
        self.assertEqual(iha.weight, data['weight'])
        self.assertEqual(iha.category, data['category'])
        self.assertEqual(iha.year, data['year'])
        self.assertEqual(iha.price, data['price'])

    def test_create_iha_invalid_data(self):
        # Geçersiz veri ile IHA oluşturma senaryosu
        url = reverse('create_iha')  # 'create_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'brand': '',  # Eksik alan
            'model': 'TestModel',
            'weight': 100,
            'category': 'TestCategory',
            'year': 2023,
            'price': 2000,
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Brand, model, weight, category, year and price are required')

    def test_update_iha_success(self):
        # IHA bilgilerini güncelleme senaryosu
        iha = IHA.objects.create(brand='TestBrand', model='TestModel', weight=100, category='TestCategory', year=2023, price=2000)
        url = reverse('update_iha', kwargs={'selected_iha_id': iha.id})  # 'update_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'brand': 'UpdatedBrand',
            'model': 'UpdatedModel',
            'weight': 150,
            'category': 'UpdatedCategory',
            'year': 2024,
            'price': 2500,
        }

        response = self.client.put(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA updated successfully')

        # Güncellenen IHA'yı kontrol et
        iha.refresh_from_db()
        self.assertEqual(iha.brand, data['brand'])
        self.assertEqual(iha.model, data['model'])
        self.assertEqual(iha.weight, data['weight'])
        self.assertEqual(iha.category, data['category'])
        self.assertEqual(iha.year, data['year'])
        self.assertEqual(iha.price, data['price'])

    def test_update_iha_invalid_data(self):
        # Geçersiz veri ile IHA bilgilerini güncelleme senaryosu
        iha = IHA.objects.create(brand='TestBrand', model='TestModel', weight=100, category='TestCategory', year=2023, price=2000)
        url = reverse('update_iha', kwargs={'selected_iha_id': iha.id})  # 'update_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'brand': '',  # Eksik alan
            'model': 'UpdatedModel',
            'weight': 150,
            'category': 'UpdatedCategory',
            'year': 2024,
            'price': 2500,
        }

        response = self.client.put(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Brand, model, weight, category, year, price and selected_iha_id are required')

    def test_delete_iha_success(self):
        # IHA silme senaryosu
        iha = IHA.objects.create(brand='TestBrand', model='TestModel', weight=100, category='TestCategory', year=2023, price=2000)
        url = reverse('delete_iha', kwargs={'selected_iha_id': iha.id})  # 'delete_iha' endpoint'inizin doğru adını kullanmalısınız

        response = self.client.delete(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA deleted successfully')

        # Silinen IHA'nın varlığını kontrol et
        self.assertFalse(IHA.objects.filter(id=iha.id).exists())

    def test_delete_iha_invalid_data(self):
        # Geçersiz veri ile IHA silme senaryosu
        iha = IHA.objects.create(brand='TestBrand', model='TestModel', weight=100, category='TestCategory', year=2023, price=2000)
        url = reverse('delete_iha', kwargs={'selected_iha_id': ''})  # 'delete_iha' endpoint'inizin doğru adını kullanmalısınız

        response = self.client.delete(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA id is required')