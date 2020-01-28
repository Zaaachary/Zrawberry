from django.urls import path

from . import views

app_name = "navigation"

urlpatterns = [
    path('', views.navigation_index, name="navigation_index"),
    path('navigation-list', views.navigation_list, name="navigation_list")
]