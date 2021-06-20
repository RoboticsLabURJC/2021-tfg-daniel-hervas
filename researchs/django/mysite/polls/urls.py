from django.urls import path
from . import views

# Espacio de nombres de la aplicación
app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
]