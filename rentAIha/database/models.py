from django.db import models

# User model 
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

# IHA model
class IHA(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight = models.IntegerField()
    category = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    is_rented = models.BooleanField(default=False)

# Rent model
class Rent(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    iha_id = models.ForeignKey(IHA, on_delete=models.CASCADE, db_column='iha_id')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
