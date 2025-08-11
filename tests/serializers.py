from rest_framework import serializers
from .models import SportTest


class SportTestSerializer(serializers.ModelSerializer):
    """
    سریالایزر تست ورزشی
    """
    duration_display = serializers.SerializerMethodField()
    cost_display = serializers.SerializerMethodField()
    reward_display = serializers.SerializerMethodField()
    collateral_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SportTest
        fields = [
            'id', 'name', 'author', 'average_duration', 'duration_display',
            'test_cost', 'cost_display', 'reward_tokens', 'reward_display',
            'collateral_count', 'collateral_display', 'sport_type', 'description', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_duration_display(self, obj):
        return obj.get_duration_display()
    
    def get_cost_display(self, obj):
        return obj.get_cost_display()
    
    def get_reward_display(self, obj):
        return obj.get_reward_display()
    
    def get_collateral_display(self, obj):
        return obj.get_collateral_display()


class SportTestCreateSerializer(serializers.ModelSerializer):
    """
    سریالایزر ایجاد تست ورزشی
    """
    class Meta:
        model = SportTest
        fields = ['name', 'author', 'average_duration', 'test_cost', 'reward_tokens', 'collateral_count', 'sport_type', 'description']
    
    def validate_average_duration(self, value):
        """
        اعتبارسنجی مدت زمان
        """
        if value.total_seconds() <= 0:
            raise serializers.ValidationError("مدت زمان باید بیشتر از صفر باشد")
        return value
    
    def validate_test_cost(self, value):
        """
        اعتبارسنجی هزینه
        """
        if value < 0:
            raise serializers.ValidationError("هزینه نمی‌تواند منفی باشد")
        return value
    
    def validate_reward_tokens(self, value):
        """
        اعتبارسنجی توکن جایزه
        """
        if value < 0:
            raise serializers.ValidationError("تعداد توکن نمی‌تواند منفی باشد")
        return value
    
    def validate_collateral_count(self, value):
        """
        اعتبارسنجی تعداد وثیقه
        """
        if value < 0:
            raise serializers.ValidationError("تعداد وثیقه نمی‌تواند منفی باشد")
        return value


class SportTestUpdateSerializer(serializers.ModelSerializer):
    """
    سریالایزر بروزرسانی تست ورزشی
    """
    class Meta:
        model = SportTest
        fields = ['name', 'author', 'average_duration', 'test_cost', 'reward_tokens', 'collateral_count', 'sport_type', 'description']
        extra_kwargs = {
            'name': {'required': False},
            'author': {'required': False},
            'average_duration': {'required': False},
            'test_cost': {'required': False},
            'reward_tokens': {'required': False},
            'collateral_count': {'required': False},
            'sport_type': {'required': False},
            'description': {'required': False}
        }
    
    def validate_average_duration(self, value):
        """
        اعتبارسنجی مدت زمان
        """
        if value and value.total_seconds() <= 0:
            raise serializers.ValidationError("مدت زمان باید بیشتر از صفر باشد")
        return value
    
    def validate_test_cost(self, value):
        """
        اعتبارسنجی هزینه
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("هزینه نمی‌تواند منفی باشد")
        return value
    
    def validate_reward_tokens(self, value):
        """
        اعتبارسنجی توکن جایزه
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("تعداد توکن نمی‌تواند منفی باشد")
        return value
    
    def validate_collateral_count(self, value):
        """
        اعتبارسنجی تعداد وثیقه
        """
        if value is not None and value < 0:
            raise serializers.ValidationError("تعداد وثیقه نمی‌تواند منفی باشد")
        return value


class SportTestDetailSerializer(serializers.ModelSerializer):
    """
    سریالایزر جزئیات تست ورزشی
    """
    duration_display = serializers.SerializerMethodField()
    cost_display = serializers.SerializerMethodField()
    reward_display = serializers.SerializerMethodField()
    collateral_display = serializers.SerializerMethodField()
    
    class Meta:
        model = SportTest
        fields = [
            'id', 'name', 'author', 'average_duration', 'duration_display',
            'test_cost', 'cost_display', 'reward_tokens', 'reward_display',
            'collateral_count', 'collateral_display', 'sport_type', 'description', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_duration_display(self, obj):
        return obj.get_duration_display()
    
    def get_cost_display(self, obj):
        return obj.get_cost_display()
    
    def get_reward_display(self, obj):
        return obj.get_reward_display()
    
    def get_collateral_display(self, obj):
        return obj.get_collateral_display()











