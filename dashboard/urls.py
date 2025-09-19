from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('tables/', views.tables, name='tables'),
]
