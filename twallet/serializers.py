from rest_framework import serializers
from .models import TokenBalance, UserBalance, BuyOrder, SellOrder, Transaction


class TokenBalanceSerializer(serializers.ModelSerializer):
    """
    سریالایزر موجودی توکن
    """
    class Meta:
        model = TokenBalance
        fields = ['total_tokens', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserBalanceSerializer(serializers.ModelSerializer):
    """
    سریالایزر موجودی کاربر
    """
    class Meta:
        model = UserBalance
        fields = ['username', 'tokens', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BuyOrderSerializer(serializers.ModelSerializer):
    """
    سریالایزر سفارش خرید
    """
    class Meta:
        model = BuyOrder
        fields = [
            'id', 'username', 'quantity', 'price_per_token', 'total_amount', 
            'status', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'total_amount', 'status', 'created_at', 'completed_at']


class SellOrderSerializer(serializers.ModelSerializer):
    """
    سریالایزر سفارش فروش
    """
    class Meta:
        model = SellOrder
        fields = [
            'id', 'username', 'quantity', 'price_per_token', 'total_amount', 
            'status', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'total_amount', 'status', 'created_at', 'completed_at']


class TransactionSerializer(serializers.ModelSerializer):
    """
    سریالایزر تراکنش
    """
    class Meta:
        model = Transaction
        fields = [
            'id', 'buyer_username', 'seller_username', 'transaction_type', 
            'quantity', 'price_per_token', 'total_amount', 
            'buyer_balance_after', 'seller_balance_after', 'created_at'
        ]
        read_only_fields = ['id', 'total_amount', 'buyer_balance_after', 'seller_balance_after', 'created_at']


class BuyOrderCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر ایجاد سفارش خرید
    """
    class Meta:
        model = BuyOrder
        fields = ['username', 'quantity']


class SellOrderCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر ایجاد سفارش فروش
    """
    class Meta:
        model = SellOrder
        fields = ['username', 'quantity']


class OrderBookSerializer(serializers.Serializer):
    """
    سریالایزر orderbook
    """
    buy_orders = BuyOrderSerializer(many=True)
    sell_orders = SellOrderSerializer(many=True)
    current_balance = TokenBalanceSerializer() 