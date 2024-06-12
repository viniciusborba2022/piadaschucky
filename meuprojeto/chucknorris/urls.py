from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_joke/', views.get_joke, name='get_joke'),
    path('save_favorite/', views.save_favorite, name='save_favorite'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
]
