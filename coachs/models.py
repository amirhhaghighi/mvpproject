from django.db import models
from datetime import date


class Coach(models.Model):
    """
    مدل مربی
    """
    first_name = models.CharField(max_length=50, verbose_name="نام")
    last_name = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    specialties = models.TextField(verbose_name="رشته‌های تخصصی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "مربی"
        verbose_name_plural = "مربیان"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class CoachSchedule(models.Model):
    """
    مدل برنامه زمانی مربی
    """
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='schedules', verbose_name="مربی")
    date = models.DateField(verbose_name="تاریخ", default=date.today)
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    athlete_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام ورزشکار")
    gym_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام باشگاه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "برنامه زمانی مربی"
        verbose_name_plural = "برنامه‌های زمانی مربیان"
        ordering = ['coach', 'date', 'start_time']
        unique_together = ['coach', 'date', 'start_time', 'end_time']
    
    def __str__(self):
        athlete_info = f" - {self.athlete_name}" if self.athlete_name else ""
        gym_info = f" - {self.gym_name}" if self.gym_name else ""
        return f"{self.coach.get_full_name()} - {self.date} {self.start_time} تا {self.end_time}{athlete_info}{gym_info}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_time >= self.end_time:
            raise ValidationError("ساعت شروع باید قبل از ساعت پایان باشد")
