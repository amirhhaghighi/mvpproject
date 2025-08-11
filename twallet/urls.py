from django.urls import path
from . import views

app_name = 'twallet'

urlpatterns = [
    # موجودی
    path('balance/', views.TokenBalanceView.as_view(), name='balance'),
    path('balance/<str:username>/', views.UserBalanceView.as_view(), name='user_balance'),
    
    # سفارشات
    path('buy/', views.BuyOrderView.as_view(), name='buy_order'),
    path('sell/', views.SellOrderView.as_view(), name='sell_order'),
    path('orders/buy/', views.BuyOrderListView.as_view(), name='buy_orders'),
    path('orders/sell/', views.SellOrderListView.as_view(), name='sell_orders'),
    
    # orderbook
    path('orderbook/', views.OrderBookView.as_view(), name='orderbook'),
    
    # تاریخچه
    path('transactions/', views.TransactionHistoryView.as_view(), name='transactions'),
] 