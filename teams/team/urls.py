from django.urls import path
from .views import index, create, modify

urlpatterns = [
    path('',  index, name='index'),
    path('create/', create, name='create'),
    path('<int:id>', modify, name='modify')
]
