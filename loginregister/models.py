from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    مدل کاربر ساده با فیلدهای ضروری
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="شماره تلفن")
    email = models.EmailField(blank=True, null=True, unique=False, verbose_name="ایمیل")
    account_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="شماره حساب")

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
    
    
