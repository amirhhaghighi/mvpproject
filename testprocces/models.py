from django.db import models
from django.conf import settings


class TestProcess(models.Model):
    """
    مدل فرآیند تست - برای ذخیره درخواست‌های پردازش تست
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    test_name = models.CharField(max_length=100, verbose_name='نام تست')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    test_duration = models.IntegerField(verbose_name='مدت زمان تست (دقیقه)')
    total_slots = models.IntegerField(verbose_name='تعداد کل اسلات‌ها')
    total_reservations = models.IntegerField(verbose_name='تعداد کل رزروها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'فرآیند تست'
        verbose_name_plural = 'فرآیندهای تست'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.test_name} - {self.created_at}"


class TestSlotResult(models.Model):
    """
    مدل نتیجه اسلات تست - برای ذخیره جزئیات هر اسلات
    """
    test_process = models.ForeignKey(
        TestProcess, 
        on_delete=models.CASCADE, 
        related_name='slot_results',
        verbose_name='فرآیند تست'
    )
    slot_start = models.TimeField(verbose_name='شروع اسلات')
    slot_end = models.TimeField(verbose_name='پایان اسلات')
    reservations_count = models.IntegerField(verbose_name='تعداد رزروها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'نتیجه اسلات تست'
        verbose_name_plural = 'نتایج اسلات‌های تست'
        ordering = ['slot_start']

    def __str__(self):
        return f"{self.test_process.test_name} - {self.slot_start}-{self.slot_end} - {self.reservations_count} رزرو"
