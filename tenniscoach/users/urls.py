from django.urls import path, re_path
from .views import *

app_name = "users"

urlpatterns = [
    path('change/', modify_profile, name='modifica_profilo'),
    path('view/<int:pk>/', CoachProfileDetailView.as_view(), name='view_profile'),
    path('dashboard/', YourCoursesListView.as_view(), name='dashboard'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile"),   

] 