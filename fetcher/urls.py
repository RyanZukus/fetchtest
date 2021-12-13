from django.urls import path
from . import views

app_name = "fetcher"
urlpatterns = [
    path('', views.main, name='main'),
    path('add/', views.add, name='add'),
    path('spend/', views.spend, name='spend'),
    path('balance/', views.balance, name='balance')
]
