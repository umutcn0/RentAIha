import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from database.models import User, IHA, Rent  # Modelleri içe aktardığınızdan emin olun
from rent.views import RentOperations

class RentOperationsTest(TestCase):
    def setUp(self):
        # Test kullanıcısını oluştur
        self.user_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
        }
        self.user = User.objects.create(**self.user_data)

        # Test IHA'sını oluştur
        self.iha_data = {
            'brand': 'TestBrand',
            'model': 'TestModel',
            'is_rented': False,
        }
        self.iha = IHA.objects.create(**self.iha_data)

        # Test kirasını oluştur
        self.rent_data = {
            'user_id': self.user,
            'iha_id': self.iha,
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=7),
            'is_active': True,
        }
        self.rent = Rent.objects.create(**self.rent_data)

    def test_get_rent_history(self):
        # Kira geçmişini almak için başarılı senaryo
        url = reverse('get_rent_history')  # 'get_rent_history' endpoint'inizin doğru adını kullanmalısınız

        response = self.client.get(url)
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response)
        self.assertIsInstance(json_response, list)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]['user_id'], 'John Doe')  # Kullanıcının adını kontrol et
        self.assertEqual(json_response[0]['iha_id'], 'TestBrand TestModel')  # IHA'nın marka ve modelini kontrol et

    def test_rent_iha_success(self):
        # IHA kiralama işlemi için başarılı senaryo
        url = reverse('rent_iha')  # 'rent_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': self.iha.id,
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now() + timedelta(days=7)),
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA rented successfully')

        # IHA'nın kiralı olup olmadığını kontrol et
        self.iha.refresh_from_db()
        self.assertTrue(self.iha.is_rented)

    def test_rent_iha_already_rented(self):
        # Zaten kiralı bir IHA'yı tekrar kiralamaya çalışma senaryosu
        url = reverse('rent_iha')  # 'rent_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': self.iha.id,
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now() + timedelta(days=7)),
        }

        # IHA'nın kiralı olduğunu işaretle
        self.iha.is_rented = True
        self.iha.save()

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA is already rented')

    def test_rent_iha_invalid_data(self):
        # Geçersiz veri ile IHA kiralama senaryosu
        url = reverse('rent_iha')  # 'rent_iha' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': '',  # Eksik alan
            'start_date': str(datetime.now()),
            'end_date': str(datetime.now() + timedelta(days=7)),
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'IHA, start date, end date and user id are required')

    def test_update_rent_success(self):
        # Kira bilgilerini güncelleme senaryosu
        url = reverse('update_rent')  # 'update_rent' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': self.rent.id,
            'start_date': str(datetime.now() - timedelta(days=1)),  # Yeni başlangıç tarihi
            'end_date': str(datetime.now() + timedelta(days=14)),  # Yeni bitiş tarihi
        }

        response = self.client.put(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'Rent updated successfully')

        # Kira bilgilerini kontrol et
        self.rent.refresh_from_db()
        self.assertEqual(str(self.rent.start_date), data['start_date'])
        self.assertEqual(str(self.rent.end_date), data['end_date'])

    def test_update_rent_invalid_data(self):
        # Geçersiz veri ile kira bilgilerini güncelleme senaryosu
        url = reverse('update_rent')  # 'update_rent' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': '',  # Eksik alan
            'start_date': str(datetime.now() - timedelta(days=1)),
            'end_date': str(datetime.now() + timedelta(days=14)),
        }

        response = self.client.put(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Rent id is required')

    def test_delete_rent_success(self):
        # Kira bilgilerini silme senaryosu
        url = reverse('delete_rent')  # 'delete_rent' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': self.rent.id,
        }

        response = self.client.delete(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'Rent deleted successfully')

        # Kira bilgisini kontrol et
        self.rent.refresh_from_db()
        self.assertFalse(self.rent.is_active)

        # IHA'nın kiralı durumunu kontrol et
        self.iha.refresh_from_db()
        self.assertFalse(self.iha.is_rented)

    def test_delete_rent_invalid_data(self):
        # Geçersiz veri ile kira bilgilerini silme senaryosu
        url = reverse('delete_rent')  # 'delete_rent' endpoint'inizin doğru adını kullanmalısınız
        data = {
            'selected_rent_id': '',  # Eksik alan
        }

        response = self.client.delete(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'User id and IHA id are required')