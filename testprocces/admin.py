from django.contrib import admin
from .models import TestProcess, TestSlotResult


@admin.register(TestProcess)
class TestProcessAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای فرآیندهای تست
    """
    list_display = ('user', 'test_name', 'start_time', 'end_time', 'test_duration', 'total_slots', 'total_reservations', 'created_at')
    list_filter = ('test_name', 'created_at', 'test_duration')
    search_fields = ('user__username', 'test_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات کاربر', {'fields': ('user',)}),
        ('اطلاعات تست', {'fields': ('test_name', 'test_duration')}),
        ('بازه زمانی', {'fields': ('start_time', 'end_time')}),
        ('آمار', {'fields': ('total_slots', 'total_reservations')}),
        ('تاریخ', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(TestSlotResult)
class TestSlotResultAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای نتایج اسلات‌های تست
    """
    list_display = ('test_process', 'slot_start', 'slot_end', 'reservations_count', 'created_at')
    list_filter = ('test_process__test_name', 'created_at')
    search_fields = ('test_process__test_name', 'test_process__user__username')
    ordering = ('test_process', 'slot_start')
    
    fieldsets = (
        ('فرآیند تست', {'fields': ('test_process',)}),
        ('بازه زمانی', {'fields': ('slot_start', 'slot_end')}),
        ('آمار', {'fields': ('reservations_count',)}),
        ('تاریخ', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
