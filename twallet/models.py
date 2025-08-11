from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class TokenBalance(models.Model):
    """
    مدل موجودی توکن‌ها (موجودی کلی سیستم)
    """
    total_tokens = models.PositiveIntegerField(
        default=0, 
        verbose_name="تعداد کل توکن‌ها",
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "موجودی توکن"
        verbose_name_plural = "موجودی توکن‌ها"

    def __str__(self):
        return f"موجودی: {self.total_tokens} توکن"

    @classmethod
    def get_balance(cls):
        """
        دریافت موجودی فعلی (همیشه یک رکورد)
        """
        balance, created = cls.objects.get_or_create(id=1)
        return balance

    def add_tokens(self, amount):
        """
        اضافه کردن توکن
        """
        self.total_tokens += amount
        self.save()

    def remove_tokens(self, amount):
        """
        کم کردن توکن
        """
        if self.total_tokens >= amount:
            self.total_tokens -= amount
            self.save()
            return True
        return False


class UserBalance(models.Model):
    """
    مدل موجودی توکن‌های هر کاربر
    """
    username = models.CharField(max_length=150, unique=True, verbose_name="نام کاربری")
    tokens = models.PositiveIntegerField(
        default=0, 
        verbose_name="تعداد توکن‌ها",
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "موجودی کاربر"
        verbose_name_plural = "موجودی کاربران"

    def __str__(self):
        return f"{self.username}: {self.tokens} توکن"

    @classmethod
    def get_or_create_balance(cls, username):
        """
        دریافت یا ایجاد موجودی کاربر
        """
        balance, created = cls.objects.get_or_create(username=username)
        return balance

    def add_tokens(self, amount):
        """
        اضافه کردن توکن به موجودی کاربر
        """
        self.tokens += amount
        self.save()

    def remove_tokens(self, amount):
        """
        کم کردن توکن از موجودی کاربر
        """
        if self.tokens >= amount:
            self.tokens -= amount
            self.save()
            return True
        return False


class BuyOrder(models.Model):
    """
    مدل سفارش خرید
    """
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]

    username = models.CharField(max_length=150, verbose_name="نام کاربری", default="unknown_user")
    quantity = models.PositiveIntegerField(
        verbose_name="تعداد توکن",
        validators=[MinValueValidator(1)]
    )
    price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1000.00'),
        verbose_name="قیمت هر توکن (تومان)"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="مبلغ کل (تومان)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تکمیل")

    class Meta:
        verbose_name = "سفارش خرید"
        verbose_name_plural = "سفارشات خرید"
        ordering = ['created_at']  # FIFO

    def __str__(self):
        return f"{self.username} - خرید {self.quantity} توکن - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """
        محاسبه خودکار مبلغ کل
        """
        if not self.total_amount:
            self.total_amount = self.quantity * self.price_per_token
        super().save(*args, **kwargs)

    def complete_order(self):
        """
        تکمیل سفارش
        """
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class SellOrder(models.Model):
    """
    مدل سفارش فروش
    """
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]

    username = models.CharField(max_length=150, verbose_name="نام کاربری", default="unknown_user")
    quantity = models.PositiveIntegerField(
        verbose_name="تعداد توکن",
        validators=[MinValueValidator(1)]
    )
    price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('1000.00'),
        verbose_name="قیمت هر توکن (تومان)"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="مبلغ کل (تومان)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ تکمیل")

    class Meta:
        verbose_name = "سفارش فروش"
        verbose_name_plural = "سفارشات فروش"
        ordering = ['created_at']  # FIFO

    def __str__(self):
        return f"{self.username} - فروش {self.quantity} توکن - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """
        محاسبه خودکار مبلغ کل
        """
        if not self.total_amount:
            self.total_amount = self.quantity * self.price_per_token
        super().save(*args, **kwargs)

    def complete_order(self):
        """
        تکمیل سفارش
        """
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()


class Transaction(models.Model):
    """
    مدل تراکنش برای ثبت تاریخچه
    """
    TRANSACTION_TYPES = [
        ('buy', 'خرید'),
        ('sell', 'فروش'),
    ]

    buyer_username = models.CharField(max_length=150, verbose_name="نام کاربری خریدار", default="unknown_user")
    seller_username = models.CharField(max_length=150, verbose_name="نام کاربری فروشنده", default="unknown_user")
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name="نوع تراکنش"
    )
    quantity = models.PositiveIntegerField(verbose_name="تعداد توکن")
    price_per_token = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="قیمت هر توکن"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="مبلغ کل"
    )
    buyer_balance_after = models.PositiveIntegerField(verbose_name="موجودی خریدار پس از تراکنش")
    seller_balance_after = models.PositiveIntegerField(verbose_name="موجودی فروشنده پس از تراکنش")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ تراکنش")

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنشات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.buyer_username} -> {self.seller_username}: {self.quantity} توکن - {self.created_at}"
