from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    # تست‌های ورزشی
    path('sport-test/list/', views.SportTestListView.as_view(), name='sport_test_list'),
    path('sport-test/create/', views.SportTestCreateView.as_view(), name='sport_test_create'),
    path('sport-test/<int:test_id>/detail/', views.SportTestDetailView.as_view(), name='sport_test_detail'),
    path('sport-test/<int:test_id>/update/', views.SportTestUpdateView.as_view(), name='sport_test_update'),
    path('sport-test/<int:test_id>/delete/', views.SportTestDeleteView.as_view(), name='sport_test_delete'),
    
    # فیلتر بر اساس نوع ورزش
    path('sport-test/sport/<str:sport_type>/', views.SportTestBySportTypeView.as_view(), name='sport_test_by_sport'),
    
    # فیلتر بر اساس نویسنده (باشگاه)
    path('sport-test/author/<str:author>/', views.SportTestByAuthorView.as_view(), name='sport_test_by_author'),
]






















