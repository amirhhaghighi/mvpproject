from django.db import models
from datetime import date


class Gym(models.Model):
    """
    مدل باشگاه ورزشی
    """
    name = models.CharField(max_length=100, verbose_name='نام باشگاه')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس')
    owner = models.CharField(max_length=100, verbose_name='صاحب باشگاه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'باشگاه'
        verbose_name_plural = 'باشگاه‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    """
    مدل بازه زمانی باشگاه
    """
    gym = models.ForeignKey(
        Gym, 
        on_delete=models.CASCADE, 
        related_name='timeslots', 
        verbose_name='باشگاه'
    )
    date = models.DateField(verbose_name='تاریخ', default=date.today)
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'بازه زمانی'
        verbose_name_plural = 'بازه‌های زمانی'
        ordering = ['date', 'start_time']
        unique_together = ['gym', 'date', 'start_time', 'end_time']

    def __str__(self):
        return f"{self.gym.name} - {self.date} {self.start_time}-{self.end_time}"
