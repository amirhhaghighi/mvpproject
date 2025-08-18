from django.urls import path
from . import views

app_name = 'coachs'

urlpatterns = [
    # مربیان
    path('coach/list/', views.CoachListView.as_view(), name='coach_list'),
    path('coach/create/', views.CoachCreateView.as_view(), name='coach_create'),
    path('coach/<str:username>/detail/', views.CoachDetailView.as_view(), name='coach_detail'),
    path('coach/<str:username>/update/', views.CoachUpdateView.as_view(), name='coach_update'),
    path('coach/<str:username>/delete/', views.CoachDeleteView.as_view(), name='coach_delete'),
    
    # برنامه‌های زمانی
    path('coach/<int:coach_id>/schedule/', views.CoachScheduleListView.as_view(), name='coach_schedule_list'),
    path('coach/<int:coach_id>/schedule/add/', views.CoachScheduleCreateView.as_view(), name='coach_schedule_create'),
    path('coach/<int:coach_id>/schedule/<int:schedule_id>/delete/', views.CoachScheduleDeleteView.as_view(), name='coach_schedule_delete'),
    
    # فیلتر بر اساس تخصص
    path('coach/specialty/<str:specialty>/', views.CoachBySpecialtyView.as_view(), name='coach_by_specialty'),
    
    # جستجوی مربیان آزاد
    path('coach/available/', views.AvailableCoachesView.as_view(), name='available_coaches'),
]




















