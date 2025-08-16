from django.urls import path
from . import views

app_name = 'testprocces'

urlpatterns = [
    # نمایش لیست تست‌های موجود
    path('tests/', views.AvailableTestsView.as_view(), name='available_tests'),
    # پردازش تست و تقسیم بازه زمانی
    path('process/', views.TestProcessView.as_view(), name='test_process'),
    path('process-gym/', views.TestProcessWithGymView.as_view(), name='test_process_with_gym'),

]
