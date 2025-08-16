from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model


from .models import TokenBalance, UserBalance, BuyOrder, SellOrder, Transaction
from .serializers import (
    TokenBalanceSerializer, UserBalanceSerializer, BuyOrderSerializer, SellOrderSerializer, 
    TransactionSerializer, BuyOrderCreateSerializer, SellOrderCreateSerializer,
    OrderBookSerializer
)

User = get_user_model()

class TokenBalanceView(APIView):
    """
    مشاهده موجودی توکن‌ها
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        balance = TokenBalance.get_balance()
        serializer = TokenBalanceSerializer(balance)
        return Response(serializer.data)


class UserBalanceView(APIView):
    """
    مشاهده موجودی کاربر
    """
    permission_classes = [AllowAny]
    
    def get(self, request, username):
        balance = UserBalance.get_or_create_balance(username)
        serializer = UserBalanceSerializer(balance)
        return Response(serializer.data)


class BuyOrderView(APIView):
    """
    ایجاد سفارش خرید
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = BuyOrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        quantity = serializer.validated_data['quantity']
        try:
         user = User.objects.get(username=username)
        except User.DoesNotExist:
           return Response(
            {"error": "کاربری با این نام کاربری وجود ندارد."},
             status=status.HTTP_400_BAD_REQUEST
    )

        
        with transaction.atomic():
            # ایجاد سفارش خرید با وضعیت pending
            buy_order = BuyOrder.objects.create(
                username=username,
                quantity=quantity,
                status='pending'
            )
            
            # بررسی سفارشات فروش موجود (FIFO)
            sell_orders = SellOrder.objects.filter(
                status='pending'
            ).order_by('created_at')
            
            remaining_quantity = quantity
            matched_orders = []
            
            for sell_order in sell_orders:
                if remaining_quantity <= 0:
                    break
                
                # محاسبه تعداد قابل معامله
                trade_quantity = min(remaining_quantity, sell_order.quantity)
                
                # بروزرسانی موجودی خریدار
                buyer_balance = UserBalance.get_or_create_balance(username)
                buyer_balance.add_tokens(trade_quantity)
                
                # بروزرسانی موجودی فروشنده
                seller_balance = UserBalance.get_or_create_balance(sell_order.username)
                seller_balance.remove_tokens(trade_quantity)
                
                # ثبت تراکنش
                Transaction.objects.create(
                    buyer_username=username,
                    seller_username=sell_order.username,
                    transaction_type='buy',
                    quantity=trade_quantity,
                    price_per_token=buy_order.price_per_token,
                    total_amount=trade_quantity * buy_order.price_per_token,
                    buyer_balance_after=buyer_balance.tokens,
                    seller_balance_after=seller_balance.tokens
                )
                
                # بروزرسانی سفارشات
                if trade_quantity == sell_order.quantity:
                    sell_order.complete_order()
                else:
                    sell_order.quantity -= trade_quantity
                    sell_order.save()
                
                remaining_quantity -= trade_quantity
                matched_orders.append(sell_order.id)
            
            # اگر هنوز توکن باقی مانده، سفارش خرید در pending می‌ماند
            if remaining_quantity > 0:
                buy_order.quantity = remaining_quantity
                buy_order.save()
            else:
                buy_order.complete_order()
            
            return Response({
                'message': 'سفارش خرید با موفقیت ثبت شد',
                'order_id': buy_order.id,
                'username': username,
                'quantity': quantity,
                'total_amount': buy_order.total_amount,
                'status': buy_order.status,
                'matched_orders': matched_orders,
                'remaining_quantity': remaining_quantity
            }, status=status.HTTP_201_CREATED)


class SellOrderView(APIView):
    """
    ایجاد سفارش فروش
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SellOrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        quantity = serializer.validated_data['quantity']
        try:
         user = User.objects.get(username=username)
        except User.DoesNotExist:
           return Response(
            {"error": "کاربری با این نام کاربری وجود ندارد."},
             status=status.HTTP_400_BAD_REQUEST
    )

        
        with transaction.atomic():
            # بررسی موجودی کافی کاربر
            user_balance = UserBalance.get_or_create_balance(username)
            if user_balance.tokens < quantity:
                return Response({
                    'error': 'موجودی کافی نیست',
                    'current_balance': user_balance.tokens,
                    'requested_quantity': quantity
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # ایجاد سفارش فروش با وضعیت pending
            sell_order = SellOrder.objects.create(
                username=username,
                quantity=quantity,
                status='pending'
            )
            
            # بررسی سفارشات خرید موجود (FIFO)
            buy_orders = BuyOrder.objects.filter(
                status='pending'
            ).order_by('created_at')
            
            remaining_quantity = quantity
            matched_orders = []
            
            for buy_order in buy_orders:
                if remaining_quantity <= 0:
                    break
                
                # محاسبه تعداد قابل معامله
                trade_quantity = min(remaining_quantity, buy_order.quantity)
                
                # کم کردن از موجودی فروشنده
                seller_balance = UserBalance.get_or_create_balance(username)
                seller_balance.remove_tokens(trade_quantity)
                
                # اضافه کردن به موجودی خریدار
                buyer_balance = UserBalance.get_or_create_balance(buy_order.username)
                buyer_balance.add_tokens(trade_quantity)
                
                # ثبت تراکنش
                Transaction.objects.create(
                    buyer_username=buy_order.username,
                    seller_username=username,
                    transaction_type='sell',
                    quantity=trade_quantity,
                    price_per_token=sell_order.price_per_token,
                    total_amount=trade_quantity * sell_order.price_per_token,
                    buyer_balance_after=buyer_balance.tokens,
                    seller_balance_after=seller_balance.tokens
                )
                
                # بروزرسانی سفارشات
                if trade_quantity == buy_order.quantity:
                    buy_order.complete_order()
                else:
                    buy_order.quantity -= trade_quantity
                    buy_order.save()
                
                remaining_quantity -= trade_quantity
                matched_orders.append(buy_order.id)
            
            # اگر هنوز توکن باقی مانده، سفارش فروش در pending می‌ماند
            if remaining_quantity > 0:
                sell_order.quantity = remaining_quantity
                sell_order.save()
            else:
                sell_order.complete_order()
            
            return Response({
                'message': 'سفارش فروش با موفقیت ثبت شد',
                'order_id': sell_order.id,
                'username': username,
                'quantity': quantity,
                'total_amount': sell_order.total_amount,
                'status': sell_order.status,
                'matched_orders': matched_orders,
                'remaining_quantity': remaining_quantity
            }, status=status.HTTP_201_CREATED)


class OrderBookView(APIView):
    """
    مشاهده orderbook
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        buy_orders = BuyOrder.objects.filter(status='pending')
        sell_orders = SellOrder.objects.filter(status='pending')
        balance = TokenBalance.get_balance()
        
        data = {
            'buy_orders': BuyOrderSerializer(buy_orders, many=True).data,
            'sell_orders': SellOrderSerializer(sell_orders, many=True).data,
            'current_balance': TokenBalanceSerializer(balance).data
        }
        
        return Response(data)


class TransactionHistoryView(generics.ListAPIView):
    """
    مشاهده تاریخچه تراکنشات
    """
    permission_classes = [AllowAny]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class BuyOrderListView(generics.ListAPIView):
    """
    مشاهده لیست سفارشات خرید
    """
    permission_classes = [AllowAny]
    queryset = BuyOrder.objects.all()
    serializer_class = BuyOrderSerializer


class SellOrderListView(generics.ListAPIView):
    """
    مشاهده لیست سفارشات فروش
    """
    permission_classes = [AllowAny]
    queryset = SellOrder.objects.all()
    serializer_class = SellOrderSerializer
