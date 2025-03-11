from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.TextField()  # Lưu hash thay vì plaintext