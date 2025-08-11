from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    مدل کاربر ساده با فیلدهای ضروری
    """
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تلفن")
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    def __str__(self):
        return f"{self.username} ({self.email})"

