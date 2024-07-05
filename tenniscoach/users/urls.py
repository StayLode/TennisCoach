from django.urls import path, re_path
from .views import *

app_name = "users"

urlpatterns = [
    # Modifica del profilo
    path('change/', modify_profile, name='modifica_profilo'),

    # Profilo coach con corsi creati
    path('view/<int:pk>/', CoachProfileDetailView.as_view(), name='view_profile'),

    # Corsi acquistati
    path('dashboard/', YourCoursesListView.as_view(), name='dashboard'),

    # Cambio password
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Profilo utenti
    path("<int:pk>/", ProfileDetailView.as_view(), name="profile"),   
] 