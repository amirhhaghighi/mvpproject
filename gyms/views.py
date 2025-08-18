from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Gym, TimeSlot
from .serializers import (
    GymSerializer, GymCreateSerializer, GymUpdateSerializer, GymDetailSerializer,
    TimeSlotSerializer, TimeSlotCreateSerializer
)


class GymListView(generics.ListAPIView):
    """
    نمایش لیست باشگاه‌ها
    """
    permission_classes = [AllowAny]
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class GymCreateView(APIView):
    """
    ایجاد باشگاه جدید
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GymCreateSerializer(data=request.data)
        if serializer.is_valid():
            gym = serializer.save()
            return Response({
                'message': 'باشگاه با موفقیت ایجاد شد',
                'gym_id': gym.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymDetailView(generics.RetrieveAPIView):
    """
    نمایش جزئیات باشگاه
    """
    permission_classes = [AllowAny]
    queryset = Gym.objects.all()
    serializer_class = GymDetailSerializer
    lookup_field = 'name'


class GymUpdateView(APIView):
    """
    بروزرسانی باشگاه
    """
    permission_classes = [AllowAny]
    
    def put(self, request, name):
        try:
            gym = Gym.objects.get(name=name)
            serializer = GymUpdateSerializer(gym, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'باشگاه با موفقیت بروزرسانی شد',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Gym.DoesNotExist:
            return Response({
                'error': 'باشگاه یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class GymDeleteView(APIView):
    """
    حذف باشگاه
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, gym_id):
        try:
            gym = Gym.objects.get(id=gym_id)
            gym.delete()
            return Response({
                'message': 'باشگاه با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except Gym.DoesNotExist:
            return Response({
                'error': 'باشگاه یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class GymTimeSlotsView(generics.ListAPIView):
    """
    نمایش بازه‌های زمانی باشگاه
    """
    permission_classes = [AllowAny]
    serializer_class = TimeSlotSerializer
    
    def get_queryset(self):
        gym_id = self.kwargs['gym_id']
        return TimeSlot.objects.filter(gym_id=gym_id)


class TimeSlotCreateView(APIView):
    """
    اضافه کردن بازه زمانی به باشگاه
    """
    permission_classes = [AllowAny]
    
    def post(self, request, gym_id):
        try:
            gym = Gym.objects.get(id=gym_id)
            serializer = TimeSlotCreateSerializer(data=request.data)
            if serializer.is_valid():
                timeslot = serializer.save(gym=gym)
                return Response({
                    'message': 'بازه زمانی با موفقیت اضافه شد',
                    'timeslot_id': timeslot.id
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Gym.DoesNotExist:
            return Response({
                'error': 'باشگاه یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class TimeSlotDeleteView(APIView):
    """
    حذف بازه زمانی
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, gym_id, timeslot_id):
        try:
            timeslot = TimeSlot.objects.get(id=timeslot_id, gym_id=gym_id)
            timeslot.delete()
            return Response({
                'message': 'بازه زمانی با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except TimeSlot.DoesNotExist:
            return Response({
                'error': 'بازه زمانی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)
