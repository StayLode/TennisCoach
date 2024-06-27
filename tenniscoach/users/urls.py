from django.urls import path, re_path
from .views import *

app_name = "users"

urlpatterns = [
	#re_path(r"^$|^\/$", , name="dash")
    path('change/', modifica_profilo, name='modifica_profilo'),
    path('view/<pk>', CoachProfileDetailView.as_view(), name='view_profile'),
    path('dashboard/', YourCoursesListView.as_view(), name='dashboard'),
    path("<pk>/", ProfileDetailView.as_view(), name="profile"),   
] 