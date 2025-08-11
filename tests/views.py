from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import SportTest
from .serializers import (
    SportTestSerializer, SportTestCreateSerializer, 
    SportTestUpdateSerializer, SportTestDetailSerializer
)


class SportTestListView(generics.ListAPIView):
    """
    نمایش لیست تست‌های ورزشی
    """
    permission_classes = [AllowAny]
    queryset = SportTest.objects.all()
    serializer_class = SportTestSerializer


class SportTestCreateView(APIView):
    """
    ایجاد تست ورزشی جدید
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SportTestCreateSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()
            return Response({
                'message': 'تست ورزشی با موفقیت ایجاد شد',
                'test_id': test.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportTestDetailView(generics.RetrieveAPIView):
    """
    نمایش جزئیات تست ورزشی
    """
    permission_classes = [AllowAny]
    queryset = SportTest.objects.all()
    serializer_class = SportTestDetailSerializer


class SportTestUpdateView(APIView):
    """
    بروزرسانی تست ورزشی
    """
    permission_classes = [AllowAny]
    
    def put(self, request, test_id):
        try:
            test = SportTest.objects.get(id=test_id)
            serializer = SportTestUpdateSerializer(test, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'تست ورزشی با موفقیت بروزرسانی شد',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SportTest.DoesNotExist:
            return Response({
                'error': 'تست ورزشی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class SportTestDeleteView(APIView):
    """
    حذف تست ورزشی
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, test_id):
        try:
            test = SportTest.objects.get(id=test_id)
            test.delete()
            return Response({
                'message': 'تست ورزشی با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except SportTest.DoesNotExist:
            return Response({
                'error': 'تست ورزشی یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class SportTestBySportTypeView(generics.ListAPIView):
    """
    نمایش تست‌های ورزشی بر اساس نوع ورزش
    """
    permission_classes = [AllowAny]
    serializer_class = SportTestSerializer
    
    def get_queryset(self):
        sport_type = self.kwargs.get('sport_type')
        return SportTest.objects.filter(sport_type=sport_type)


class SportTestByAuthorView(generics.ListAPIView):
    """
    نمایش تست‌های ورزشی بر اساس نویسنده (باشگاه)
    """
    permission_classes = [AllowAny]
    serializer_class = SportTestSerializer
    
    def get_queryset(self):
        author = self.kwargs.get('author')
        return SportTest.objects.filter(author__icontains=author)
