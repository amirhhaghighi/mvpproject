from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import CustomUser
from .serilizers import (
    UserRegistrationSerializer, UserLoginSerializer, 
    UserUpdateSerializer, UserDetailSerializer
)


class UserRegistrationView(APIView):
    """
    ثبت‌نام کاربر
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'ثبت‌نام با موفقیت انجام شد',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    ورود کاربر
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'ورود موفقیت‌آمیز بود',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    خروج کاربر
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': 'خروج موفقیت‌آمیز بود'
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """
    نمایش لیست کاربران
    """
    permission_classes = [AllowAny]  # همه می‌توانند لیست کاربران را ببینند
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer


class UserDetailView(generics.RetrieveAPIView):
    """
    نمایش جزئیات کاربر
    """
    permission_classes = [AllowAny]  # همه می‌توانند جزئیات کاربران را ببینند
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateView(APIView):
    """
    بروزرسانی اطلاعات کاربر
    """
    permission_classes = [AllowAny]  # همه می‌توانند کاربران را آپدیت کنند
    
    def put(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'اطلاعات با موفقیت بروزرسانی شد',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'کاربر یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


class UserDeleteView(APIView):
    """
    حذف کاربر
    """
    permission_classes = [AllowAny]  # همه می‌توانند کاربران را حذف کنند
    
    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return Response({
                'message': 'کاربر با موفقیت حذف شد'
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                'error': 'کاربر یافت نشد'
            }, status=status.HTTP_404_NOT_FOUND)


# ویوهای ساده برای صفحات وب
@login_required
def profile_view(request):
    """
    صفحه پروفایل
    """
    return render(request, 'loginregister/profile.html', {
        'user': request.user
    })


def login_page(request):
    """
    صفحه ورود
    """
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'loginregister/login.html')


def register_page(request):
    """
    صفحه ثبت‌نام
    """
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'loginregister/register.html')
