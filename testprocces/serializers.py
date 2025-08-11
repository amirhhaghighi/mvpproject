from rest_framework import serializers
from .models import TestProcess, TestSlotResult
from tests.models import SportTest
from datetime import date


class TestProcessRequestSerializer(serializers.Serializer):
    """
    سریالایزر برای درخواست پردازش تست
    """
    username = serializers.CharField(max_length=150, help_text='نام کاربری')
    test_name = serializers.CharField(max_length=100, help_text='نام تست')
    start_time = serializers.TimeField(help_text='ساعت شروع (HH:MM)')
    end_time = serializers.TimeField(help_text='ساعت پایان (HH:MM)')
    test_date = serializers.DateField(help_text='تاریخ تست (YYYY-MM-DD)', required=False, default=date.today)

    def validate(self, data):
        """
        اعتبارسنجی بازه زمانی
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time >= end_time:
            raise serializers.ValidationError("ساعت شروع باید قبل از ساعت پایان باشد")
        
        return data
    
    def validate_test_name(self, value):
        """
        اعتبارسنجی وجود تست
        """
        if not SportTest.objects.filter(name=value).exists():
            raise serializers.ValidationError("تست با این نام یافت نشد")
        return value


class TestSlotResultSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نتیجه اسلات تست
    """
    class Meta:
        model = TestSlotResult
        fields = ['slot_start', 'slot_end', 'reservations_count']


class TestProcessResponseSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای پاسخ پردازش تست
    """
    username = serializers.CharField(source='user.username', read_only=True)
    time_slots = TestSlotResultSerializer(source='slot_results', many=True, read_only=True)
    
    class Meta:
        model = TestProcess
        fields = [
            'username', 'test_name', 'test_duration', 
            'time_slots', 'total_slots', 'total_reservations'
        ]
