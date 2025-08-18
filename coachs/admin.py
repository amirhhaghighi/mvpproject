from django.contrib import admin
from .models import Coach, CoachSchedule


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مربیان
    """
    list_display = ('first_name', 'last_name','account_number','username', 'specialties', 'phone_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'specialties', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات مربی', {'fields': ('first_name', 'last_name', 'specialties', 'phone_number')}),
        ('تاریخ‌ها', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CoachSchedule)
class CoachScheduleAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای برنامه‌های زمانی مربیان
    """
    list_display = ('coach', 'date', 'start_time', 'end_time', 'athlete_name', 'gym_name', 'created_at')
    list_filter = ('date', 'coach', 'created_at')
    search_fields = ('coach__first_name', 'coach__last_name', 'athlete_name', 'gym_name')
    ordering = ('coach', 'date', 'start_time')
    
    fieldsets = (
        ('اطلاعات برنامه زمانی', {'fields': ('coach', 'date', 'start_time', 'end_time', 'athlete_name', 'gym_name')}),
        ('تاریخ ایجاد', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
