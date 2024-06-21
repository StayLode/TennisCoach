from django.urls import path, re_path
from .views import *

app_name = "users"

urlpatterns = [
	#re_path(r"^$|^\/$", , name="dash")
    path('modifica_profilo/', modifica_profilo, name='modifica_profilo'),
    path("<pk>/", ProfileDetailView.as_view(), name="profile"),   
] 