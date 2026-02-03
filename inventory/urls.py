from django.contrib import admin
from django.urls import path
#from inventory import views
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('records/', views.records, name='records'),
    path('add_record/', views.add_record, name='add_record'),
]