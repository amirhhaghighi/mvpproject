from django.contrib import admin
from .models import SportTest


@admin.register(SportTest)
class SportTestAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای تست‌های ورزشی
    """
    list_display = ('name', 'author', 'sport_type', 'average_duration', 'test_cost', 'reward_tokens', 'collateral_count', 'created_at')
    list_filter = ('sport_type', 'created_at', 'test_cost', 'reward_tokens', 'collateral_count')
    search_fields = ('name', 'author', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('اطلاعات تست', {
            'fields': ('name', 'author', 'sport_type', 'average_duration', 'description')
        }),
        ('هزینه و جایزه', {
            'fields': ('test_cost', 'reward_tokens', 'collateral_count')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def get_duration_display(self, obj):
        return obj.get_duration_display()
    get_duration_display.short_description = 'مدت زمان'
    
    def get_cost_display(self, obj):
        return obj.get_cost_display()
    get_cost_display.short_description = 'هزینه'
    
    def get_reward_display(self, obj):
        return obj.get_reward_display()
    get_reward_display.short_description = 'جایزه'
    
    def get_collateral_display(self, obj):
        return obj.get_collateral_display()
    get_collateral_display.short_description = 'تعداد وثیقه'
