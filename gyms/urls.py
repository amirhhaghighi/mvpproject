from django.urls import path
from . import views

app_name = 'gyms'

urlpatterns = [
    # باشگاه‌ها
    path('gym/list/', views.GymListView.as_view(), name='gym_list'),
    path('gym/create/', views.GymCreateView.as_view(), name='gym_create'),
    path('gym/<int:pk>/detail/', views.GymDetailView.as_view(), name='gym_detail'),
    path('gym/<int:pk>/update/', views.GymUpdateView.as_view(), name='gym_update'),
    path('gym/<int:pk>/delete/', views.GymDeleteView.as_view(), name='gym_delete'),
    
    # بازه‌های زمانی
    path('gym/<int:gym_id>/timeslots/', views.GymTimeSlotsView.as_view(), name='gym_timeslots'),
    path('gym/<int:gym_id>/timeslot/add/', views.TimeSlotCreateView.as_view(), name='timeslot_create'),
    path('gym/<int:gym_id>/timeslot/<int:timeslot_id>/delete/', views.TimeSlotDeleteView.as_view(), name='timeslot_delete'),
]












