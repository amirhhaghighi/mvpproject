from django.urls import path
from . import views

app_name = 'loginregister'

urlpatterns = [
    # API endpoints
    path('api/register/', views.UserRegistrationView.as_view(), name='api_register'),
    path('api/login/', views.UserLoginView.as_view(), name='api_login'),
    path('api/logout/', views.UserLogoutView.as_view(), name='api_logout'),
    path('api/users/', views.UserListView.as_view(), name='api_users'),
    path('api/users/<int:user_id>/', views.UserDetailView.as_view(), name='api_user_detail'),
    path('api/users/<int:user_id>/update/', views.UserUpdateView.as_view(), name='api_user_update'),
    path('api/users/<int:user_id>/delete/', views.UserDeleteView.as_view(), name='api_user_delete'),
    
    # Web interface pages
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.profile_view, name='profile'),
]
