from rest_framework import serializers
from .models import Gym, TimeSlot


class GymSerializer(serializers.ModelSerializer):
    """
    سریالایزر اصلی برای باشگاه (لیست)
    """
    class Meta:
        model = Gym
        fields = ['id', 'name', 'phone', 'address', 'owner',' account_number', 'created_at']


class GymCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای ایجاد باشگاه جدید
    """
    class Meta:
        model = Gym
        fields = ['name', 'phone', 'address','account_number', 'owner']


class GymUpdateSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای بروزرسانی باشگاه
    """
    class Meta:
        model = Gym
        fields = ['name', 'phone', 'address','account_number', 'owner']


class GymDetailSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نمایش جزئیات باشگاه
    """
    timeslots_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Gym
        fields = ['id', 'name', 'phone', 'address','account_number', 'owner', 'created_at', 'updated_at', 'timeslots_count']
    
    def get_timeslots_count(self, obj):
        return obj.timeslots.count()


class TimeSlotSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای بازه‌های زمانی
    """
    gym_name = serializers.CharField(source='gym.name', read_only=True)
    
    class Meta:
        model = TimeSlot
        fields = ['id', 'gym', 'gym_name', 'date', 'start_time', 'end_time', 'created_at']


class TimeSlotCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای ایجاد بازه زمانی جدید
    """
    class Meta:
        model = TimeSlot
        fields = ['date', 'start_time', 'end_time']
    
    def validate(self, data):
        """
        اعتبارسنجی برای جلوگیری از تداخل بازه‌های زمانی
        """
        gym = data.get('gym')
        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time >= end_time:
            raise serializers.ValidationError("ساعت شروع باید قبل از ساعت پایان باشد")
        
        # بررسی تداخل با بازه‌های زمانی موجود
        existing_timeslots = TimeSlot.objects.filter(
            gym=gym,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if existing_timeslots.exists():
            raise serializers.ValidationError("این بازه زمانی با بازه‌های موجود تداخل دارد")
        
        return data
