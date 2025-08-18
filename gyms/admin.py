from django.contrib import admin
from .models import Gym, TimeSlot


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای باشگاه‌ها
    """
    list_display = ('name', 'owner', 'phone','account_number', 'address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner', 'phone', 'address')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات باشگاه', {'fields': ('name', 'owner', 'phone', 'address')}),
        ('تاریخ‌ها', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای بازه‌های زمانی
    """
    list_display = ('gym', 'date', 'start_time', 'end_time', 'created_at')
    list_filter = ('date', 'gym', 'created_at')
    search_fields = ('gym__name',)
    ordering = ('gym', 'date', 'start_time')
    
    fieldsets = (
        ('اطلاعات بازه زمانی', {'fields': ('gym', 'date', 'start_time', 'end_time')}),
        ('تاریخ ایجاد', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
