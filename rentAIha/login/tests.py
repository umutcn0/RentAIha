import json
from django.test import TestCase
from django.urls import reverse
from login.views import RegisterHandler, LoginHandler
from database.models import User

class LoginHandlerTest(TestCase):
    def setUp(self):
        # Test kullanıcısını oluştur
        self.user_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
        }
        User.objects.create(**self.user_data)

    def test_login_user_success(self):
        # Başarılı giriş senaryosu
        url = reverse('login')
        data = {
            'email': 'john.doe@example.com',
            'password': 'securepassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'User logged in successfully')

    def test_login_user_missing_fields(self):
        # Eksik alanlarla giriş senaryosu
        url = reverse('login')  
        data = {
            'email': 'john.doe@example.com',
            'password': '',  # Eksik alan
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Email and password are required')

    def test_login_user_incorrect_credentials(self):
        # Yanlış kimlik bilgileriyle giriş senaryosu
        url = reverse('login')  
        data = {
            'email': 'john.doe@example.com',
            'password': 'wrongpassword',  # Yanlış şifre
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Email or password is incorrect')

    def test_login_user_set_cookie(self):
        # Giriş yapıldığında cookie'nin doğru bir şekilde ayarlanması senaryosu
        url = reverse('login')  
        data = {
            'email': 'john.doe@example.com',
            'password': 'securepassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'User logged in successfully')

        # Cookie'nin varlığını ve değerini kontrol et
        self.assertIn('user_mail', response.cookies)
        self.assertEqual(response.cookies['user_mail'].value, 'john.doe@example.com')


class RegisterHandlerTest(TestCase):
    def test_register_user_success(self):
        # Örnek bir başarılı kayıt senaryosu
        url = reverse('register')
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword',
            'passwordValidate': 'securepassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['message'], 'User created successfully')

    def test_register_user_missing_fields(self):
        # Zorunlu alanların eksik olduğu senaryo
        url = reverse('register')  
        data = {
            'name': 'John Doe',
            'email': '',  # Eksik alan
            'password': 'securepassword',
            'passwordValidate': 'securepassword',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Name, email and password are required')

    def test_register_user_existing_user(self):
        # Var olan bir kullanıcıyla kayıt senaryosu
        url = reverse('register')  
        data = {
            'name': 'John Doe',
            'email': 'existing.user@example.com',
            'password': 'securepassword',
            'passwordValidate': 'securepassword',
        }

        # Önceden kullanıcı oluştur
        User.objects.create(name=data['name'], email=data['email'], password=data['password'])

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'User already exists')

    def test_register_user_weak_password(self):
        # Zayıf bir şifre kullanılarak kayıt senaryosu
        url = reverse('register')  
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'password': 'weak',  # Zayıf şifre
            'passwordValidate': 'weak',
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(json_response['success'])
        self.assertEqual(json_response['message'], 'Something went wrong with your password')
