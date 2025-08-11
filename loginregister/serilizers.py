from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    سریالایزر ثبت‌نام کاربر
    """
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(
        required=False, 
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="شماره تلفن باید در فرمت صحیح وارد شود. مثال: +989123456789 یا 09123456789"
            )
        ],
        help_text="شماره تلفن (اختیاری)"
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'phone_number': {'required': False, 'allow_blank': True}
        }
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("رمز عبور و تکرار آن یکسان نیستند")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    سریالایزر ورود کاربر
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            data['user'] = user
        else:
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    سریالایزر بروزرسانی کاربر
    """
    phone_number = serializers.CharField(
        required=False, 
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="شماره تلفن باید در فرمت صحیح وارد شود. مثال: +989123456789 یا 09123456789"
            )
        ]
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'phone_number': {'required': False, 'allow_blank': True}
        }


class UserDetailSerializer(serializers.ModelSerializer):
    """
    سریالایزر نمایش جزئیات کاربر
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_joined']
        read_only_fields = ['id', 'date_joined']
