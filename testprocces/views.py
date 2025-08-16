from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta, date
import math

from .models import TestProcess, TestSlotResult
from .serializers import TestProcessRequestSerializer, TestProcessResponseSerializer
from gyms.models import TimeSlot, Gym
from tests.models import SportTest
from tests.serializers import SportTestSerializer

# استفاده از مدل کاربر سفارشی
User = get_user_model()


class AvailableTestsView(generics.ListAPIView):
    """
    نمایش لیست تست‌های موجود
    """
    permission_classes = [AllowAny]
    queryset = SportTest.objects.all()
    serializer_class = SportTestSerializer


class TestProcessView(APIView):
    """
    ویو اصلی برای پردازش تست و تقسیم بازه زمانی
    """
    permission_classes = [AllowAny]


    
    def post(self, request):
        """
        پردازش درخواست تست و تقسیم بازه زمانی
        """
        serializer = TestProcessRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # دریافت داده‌های ورودی
        username = serializer.validated_data['username']
        test_name = serializer.validated_data['test_name']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        test_date = serializer.validated_data.get('test_date', date.today())  # تاریخ تست
        
        try:
            # پیدا کردن کاربر
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'error': 'کاربر یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # پیدا کردن تست و دریافت مدت زمان واقعی
            test = SportTest.objects.get(name=test_name)
            # تبدیل DurationField به دقیقه
            test_duration = int(test.average_duration.total_seconds() / 60)
            gym_author = test.author  # نام باشگاه نویسنده تست
        except SportTest.DoesNotExist:
            return Response({
                'error': 'تست یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # محاسبه اسلات‌های زمانی
        slots = self._calculate_time_slots(start_time, end_time, test_duration)
        
        # شمارش رزروها در هر اسلات از باشگاه نویسنده تست
        slots_with_reservations = self._count_reservations_in_slots(slots, gym_author, test_date)
        
        # محاسبه آمار کلی
        total_slots = len(slots_with_reservations)
        total_reservations = sum(slot['reservations_count'] for slot in slots_with_reservations)
        
        # ذخیره در دیتابیس
        test_process = TestProcess.objects.create(
            user=user,
            test_name=test_name,
            start_time=start_time,
            end_time=end_time,
            test_duration=test_duration,
            total_slots=total_slots,
            total_reservations=total_reservations
        )
        
        # ذخیره نتایج اسلات‌ها
        for slot in slots_with_reservations:
            TestSlotResult.objects.create(
                test_process=test_process,
                slot_start=slot['slot_start'],
                slot_end=slot['slot_end'],
                reservations_count=slot['reservations_count']
            )
        
        # بازگرداندن نتیجه
        response_serializer = TestProcessResponseSerializer(test_process)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    def _calculate_time_slots(self, start_time, end_time, duration_minutes):
        """
        تقسیم بازه زمانی به اسلات‌های کوچکتر
        """
        slots = []
        current_time = start_time
        
        while current_time < end_time:
            slot_end = self._add_minutes(current_time, duration_minutes)
            
            # اگر اسلات از بازه خارج شود، آن را محدود کن
            if slot_end > end_time:
                slot_end = end_time
            
            slots.append({
                'slot_start': current_time,
                'slot_end': slot_end
            })
            
            current_time = slot_end
        
        return slots
    
    def _add_minutes(self, time_obj, minutes):
        """
        اضافه کردن دقیقه به زمان
        """
        datetime_obj = datetime.combine(datetime.today(), time_obj)
        new_datetime = datetime_obj + timedelta(minutes=minutes)
        return new_datetime.time()
    
    def _count_reservations_in_slots(self, slots, gym_author, test_date):
        """
        شمارش رزروهای موجود در باشگاه نویسنده تست برای تاریخ مشخص
        """
        slots_with_reservations = []
        
        for slot in slots:
            # پیدا کردن رزروهای موجود در باشگاه نویسنده تست برای تاریخ مشخص
            # بررسی تداخل زمانی بین اسلات و رزروهای موجود در باشگاه
            reservations = TimeSlot.objects.filter(
                gym__name=gym_author,  # فقط باشگاه نویسنده تست
                date=test_date,  # تاریخ مشخص
                start_time__lt=slot['slot_end'],
                end_time__gt=slot['slot_start']
            ).count()
            
            slots_with_reservations.append({
                'slot_start': slot['slot_start'],
                'slot_end': slot['slot_end'],
                'reservations_count': reservations  # تعداد رزروهای موجود در باشگاه
            })
        
        return slots_with_reservations
from .serializers import TestProcessRequestSerializer, TestProcessResponseSerializer, TestProcessWithGymRequestSerializer  # اضافه کردن سریالایزر جدید

class TestProcessWithGymView(APIView):
    """
    ویو برای پردازش تست با مشخص کردن باشگاه
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        پردازش درخواست تست برای باشگاه مشخص
        """
        serializer = TestProcessWithGymRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # دریافت داده‌های ورودی
        username = serializer.validated_data['username']
        test_name = serializer.validated_data['test_name']
        gym_name = serializer.validated_data['gym_name']  # فیلد جدید
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        test_date = serializer.validated_data.get('test_date', date.today())
        
        try:
            # پیدا کردن کاربر
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                'error': 'کاربر یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # پیدا کردن تست و دریافت مدت زمان واقعی
            test = SportTest.objects.get(name=test_name)
            test_duration = int(test.average_duration.total_seconds() / 60)
        except SportTest.DoesNotExist:
            return Response({
                'error': 'تست یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # محاسبه اسلات‌های زمانی
        slots = self._calculate_time_slots(start_time, end_time, test_duration)
        
        # شمارش رزروها در هر اسلات از باشگاه مشخص شده
        slots_with_reservations = self._count_reservations_in_specific_gym(slots, gym_name, test_date)
        
        # محاسبه آمار کلی
        total_slots = len(slots_with_reservations)
        total_reservations = sum(slot['reservations_count'] for slot in slots_with_reservations)
        
        # ذخیره در دیتابیس
        test_process = TestProcess.objects.create(
            user=user,
            test_name=test_name,
            start_time=start_time,
            end_time=end_time,
            test_duration=test_duration,
            total_slots=total_slots,
            total_reservations=total_reservations
        )
        
        # ذخیره نتایج اسلات‌ها
        for slot in slots_with_reservations:
            TestSlotResult.objects.create(
                test_process=test_process,
                slot_start=slot['slot_start'],
                slot_end=slot['slot_end'],
                reservations_count=slot['reservations_count']
            )
        
        # بازگرداندن نتیجه
        response_serializer = TestProcessResponseSerializer(test_process)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    def _count_reservations_in_specific_gym(self, slots, gym_name, test_date):
        """
        شمارش رزروهای موجود در باشگاه مشخص شده برای تاریخ مشخص
        """
        slots_with_reservations = []
        
        for slot in slots:
            reservations = TimeSlot.objects.filter(
                gym__name=gym_name,  # باشگاه مشخص شده توسط کاربر
                date=test_date,
                start_time__lt=slot['slot_end'],
                end_time__gt=slot['slot_start']
            ).count()
            
            slots_with_reservations.append({
                'slot_start': slot['slot_start'],
                'slot_end': slot['slot_end'],
                'reservations_count': reservations
            })
        
        return slots_with_reservations
    
    # متدهای کمکی مشترک (کپی از کلاس قبلی)
    def _calculate_time_slots(self, start_time, end_time, duration_minutes):
        """
        تقسیم بازه زمانی به اسلات‌های کوچکتر
        """
        slots = []
        current_time = start_time
        
        while current_time < end_time:
            slot_end = self._add_minutes(current_time, duration_minutes)
            
            if slot_end > end_time:
                slot_end = end_time
            
            slots.append({
                'slot_start': current_time,
                'slot_end': slot_end
            })
            
            current_time = slot_end
        
        return slots
    
    def _add_minutes(self, time_obj, minutes):
        """
        اضافه کردن دقیقه به زمان
        """
        datetime_obj = datetime.combine(datetime.today(), time_obj)
        new_datetime = datetime_obj + timedelta(minutes=minutes)
        return new_datetime.time()