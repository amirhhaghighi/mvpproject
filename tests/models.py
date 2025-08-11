from django.db import models


class SportTest(models.Model):
    """
    مدل تست ورزشی
    """
    SPORT_CHOICES = [
        ('فوتبال', 'فوتبال'),
        ('بسکتبال', 'بسکتبال'),
        ('والیبال', 'والیبال'),
        ('تنیس', 'تنیس'),
        ('شنا', 'شنا'),
        ('دوومیدانی', 'دوومیدانی'),
        ('وزنه‌برداری', 'وزنه‌برداری'),
        ('کشتی', 'کشتی'),
        ('بوکس', 'بوکس'),
        ('کاراته', 'کاراته'),
        ('تکواندو', 'تکواندو'),
        ('جودو', 'جودو'),
        ('ژیمناستیک', 'ژیمناستیک'),
        ('اسکی', 'اسکی'),
        ('سایر', 'سایر'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="نام تست")
    author = models.CharField(max_length=100, verbose_name="نویسنده (نام باشگاه)")
    average_duration = models.DurationField(verbose_name="مدت زمان میانگین تست")
    test_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="هزینه تست (تومان)",
        default=0.00
    )
    reward_tokens = models.PositiveIntegerField(
        verbose_name="تعداد توکن جایزه",
        default=0
    )
    collateral_count = models.PositiveIntegerField(
        verbose_name="تعداد وثیقه",
        default=0
    )
    sport_type = models.CharField(
        max_length=20, 
        choices=SPORT_CHOICES, 
        verbose_name="نوع ورزش تست"
    )
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    class Meta:
        verbose_name = "تست ورزشی"
        verbose_name_plural = "تست‌های ورزشی"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.sport_type} - {self.author}"
    
    def get_duration_display(self):
        """
        نمایش مدت زمان به صورت خوانا
        """
        total_seconds = int(self.average_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours} ساعت {minutes} دقیقه {seconds} ثانیه"
        elif minutes > 0:
            return f"{minutes} دقیقه {seconds} ثانیه"
        else:
            return f"{seconds} ثانیه"
    
    def get_cost_display(self):
        """
        نمایش هزینه به صورت خوانا
        """
        return f"{self.test_cost:,} تومان"
    
    def get_reward_display(self):
        """
        نمایش جایزه به صورت خوانا
        """
        return f"{self.reward_tokens} توکن"
    
    def get_collateral_display(self):
        """
        نمایش تعداد وثیقه به صورت خوانا
        """
        return f"{self.collateral_count} وثیقه"
