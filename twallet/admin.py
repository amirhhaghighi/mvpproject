from django.contrib import admin
from .models import TokenBalance, UserBalance, BuyOrder, SellOrder, Transaction


@admin.register(TokenBalance)
class TokenBalanceAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای موجودی توکن
    """
    list_display = ('total_tokens', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # فقط یک رکورد موجودی وجود دارد
        return not TokenBalance.objects.exists()


@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای موجودی کاربران
    """
    list_display = ('username', 'tokens', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('username',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-tokens',)


@admin.register(BuyOrder)
class BuyOrderAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای سفارشات خرید
    """
    list_display = ('id', 'username', 'quantity', 'price_per_token', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'username')
    readonly_fields = ('total_amount', 'created_at', 'completed_at')
    ordering = ('-created_at',)


@admin.register(SellOrder)
class SellOrderAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای سفارشات فروش
    """
    list_display = ('id', 'username', 'quantity', 'price_per_token', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'username')
    readonly_fields = ('total_amount', 'created_at', 'completed_at')
    ordering = ('-created_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای تراکنشات
    """
    list_display = ('id', 'buyer_username', 'seller_username', 'transaction_type', 'quantity', 'price_per_token', 'total_amount', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('id', 'buyer_username', 'seller_username')
    readonly_fields = ('total_amount', 'buyer_balance_after', 'seller_balance_after', 'created_at')
    ordering = ('-created_at',)
