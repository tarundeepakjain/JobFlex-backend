from django.urls import path
from .views import application_list, application_detail

urlpatterns = [
    path('', application_list, name='application-list'),
    path('<int:app_id>/', application_detail, name='application-detail'),
]