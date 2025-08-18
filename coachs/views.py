from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from datetime import datetime, time
from django.db.models import Q

from .models import Coach, CoachSchedule
from .serializers import (
    CoachSerializer, CoachCreateSerializer, CoachUpdateSerializer, CoachDetailSerializer,
    CoachScheduleSerializer, CoachScheduleCreateSerializer
)


class CoachListView(generics.ListAPIView):
    """
    نمایش لیست مربیان
    """
    permission_classes = [AllowAny]
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class CoachCreateView(APIView):
    """
    ایجاد مربی جدید
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CoachCreateSerializer(data=request.data)
        if serializer.is_valid():
            coach = serializer.save()
            return Response({
                'message': 'مربی با موفقیت ایجاد شد',
                'coach_id': coach.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachDetailView(generics.RetrieveAPIView):
    """
    نمایش جزئیات مربی
    """
    permission_classes = [AllowAny]
    queryset = Coach.objects.all()
    serializer_class = CoachDetailSerializer
    lookup_field = 'username'



class CoachUpdateView(APIView):
    """
    بروزرسانی مربی
    """
    permission_classes = [AllowAny]
    
    def put(self, request,username):
        try:
            coach = Coach.objects.get(username=username)
            serializer = CoachUpdateSerializer(coach, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'مربی با موفقیت بروزرسانی شد',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Coach.DoesNotExist:
            return Response({
                'error': 'مربی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class CoachDeleteView(APIView):
    """
    حذف مربی
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, coach_id):
        try:
            coach = Coach.objects.get(id=coach_id)
            coach.delete()
            return Response({
                'message': 'مربی با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except Coach.DoesNotExist:
            return Response({
                'error': 'مربی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class CoachScheduleListView(generics.ListAPIView):
    """
    نمایش برنامه‌های زمانی مربی
    """
    permission_classes = [AllowAny]
    serializer_class = CoachScheduleSerializer
    
    def get_queryset(self):
        coach_id = self.kwargs['coach_id']
        return CoachSchedule.objects.filter(coach_id=coach_id)


class CoachScheduleCreateView(APIView):
    """
    اضافه کردن برنامه زمانی به مربی
    """
    permission_classes = [AllowAny]
    
    def post(self, request, coach_id):
        try:
            coach = Coach.objects.get(id=coach_id)
            serializer = CoachScheduleCreateSerializer(data=request.data)
            if serializer.is_valid():
                schedule = serializer.save(coach=coach)
                return Response({
                    'message': 'برنامه زمانی با موفقیت اضافه شد',
                    'schedule_id': schedule.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Coach.DoesNotExist:
            return Response({
                'error': 'مربی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class CoachScheduleDeleteView(APIView):
    """
    حذف برنامه زمانی
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, coach_id, schedule_id):
        try:
            schedule = CoachSchedule.objects.get(id=schedule_id, coach_id=coach_id)
            schedule.delete()
            return Response({
                'message': 'برنامه زمانی با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except CoachSchedule.DoesNotExist:
            return Response({
                'error': 'برنامه زمانی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class CoachBySpecialtyView(generics.ListAPIView):
    """
    نمایش مربیان بر اساس تخصص
    """
    permission_classes = [AllowAny]
    serializer_class = CoachSerializer
    
    def get_queryset(self):
        specialty = self.kwargs.get('specialty')
        return Coach.objects.filter(specialties__icontains=specialty)


class AvailableCoachesView(APIView):
    """
    جستجوی مربیان آزاد در بازه زمانی مشخص
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # دریافت پارامترها از درخواست
            date_str = request.data.get('date')
            start_time_str = request.data.get('start_time')
            end_time_str = request.data.get('end_time')
            
            # بررسی وجود پارامترهای ضروری
            if not all([date_str, start_time_str, end_time_str]):
                return Response({
                    'error': 'پارامترهای date، start_time و end_time الزامی هستند'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # تبدیل تاریخ و زمان
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                start_time = datetime.strptime(start_time_str, '%H:%M').time()
                end_time = datetime.strptime(end_time_str, '%H:%M').time()
            except ValueError:
                return Response({
                    'error': 'فرمت تاریخ یا زمان نامعتبر است. فرمت صحیح: YYYY-MM-DD برای تاریخ و HH:MM برای زمان'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # بررسی منطقی بودن بازه زمانی
            if start_time >= end_time:
                return Response({
                    'error': 'ساعت شروع باید قبل از ساعت پایان باشد'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # دریافت تمام مربیان
            all_coaches = Coach.objects.all()
            available_coaches = []
            
            for coach in all_coaches:
                # بررسی برنامه‌های مربی در تاریخ مشخص
                coach_schedules = CoachSchedule.objects.filter(
                    coach=coach,
                    date=date_obj
                )
                
                # بررسی تداخل زمانی
                is_available = True
                for schedule in coach_schedules:
                    # اگر بازه زمانی درخواستی با برنامه مربی تداخل داشته باشد
                    if not (end_time <= schedule.start_time or start_time >= schedule.end_time):
                        is_available = False
                        break
                
                if is_available:
                    available_coaches.append({
                        'id': coach.id,
                        'first_name': coach.first_name,
                        'last_name': coach.last_name,
                        'full_name': coach.get_full_name(),
                        'specialties': coach.specialties,
                        'phone_number': coach.phone_number
                    })
            
            return Response({
                'message': f'مربیان آزاد در تاریخ {date_str} از ساعت {start_time_str} تا {end_time_str}',
                'date': date_str,
                'start_time': start_time_str,
                'end_time': end_time_str,
                'available_coaches_count': len(available_coaches),
                'available_coaches': available_coaches
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'خطا در پردازش درخواست: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
