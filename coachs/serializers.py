from rest_framework import serializers
from .models import Coach, CoachSchedule


class CoachScheduleSerializer(serializers.ModelSerializer):
    """
    سریالایزر برنامه زمانی مربی
    """
    class Meta:
        model = CoachSchedule
        fields = ['id', 'date', 'start_time', 'end_time', 'athlete_name', 'gym_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CoachSerializer(serializers.ModelSerializer):
    """
    سریالایزر مربی
    """
    schedules = CoachScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name', 'specialties', 'phone_number', 'schedules', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoachCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر ایجاد مربی
    """
    class Meta:
        model = Coach
        fields = ['first_name', 'last_name', 'specialties', 'phone_number']


class CoachUpdateSerializer(serializers.ModelSerializer):
    """
    سریالایزر بروزرسانی مربی
    """
    class Meta:
        model = Coach
        fields = ['first_name', 'last_name', 'specialties', 'phone_number']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'specialties': {'required': False},
            'phone_number': {'required': False}
        }


class CoachDetailSerializer(serializers.ModelSerializer):
    """
    سریالایزر جزئیات مربی با برنامه‌های زمانی
    """
    schedules = CoachScheduleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Coach
        fields = ['id', 'first_name', 'last_name', 'specialties', 'phone_number', 'schedules', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoachScheduleCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر ایجاد برنامه زمانی
    """
    class Meta:
        model = CoachSchedule
        fields = ['date', 'start_time', 'end_time', 'athlete_name', 'gym_name']
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("ساعت شروع باید قبل از ساعت پایان باشد")
        return data












