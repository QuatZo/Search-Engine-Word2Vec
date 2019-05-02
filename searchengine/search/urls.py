from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_text, name='get_text'),
    # path('table.html', views.get_table, name='get_table')
]
