from django.urls import path

from . import views

app_name = "navigation"

urlpatterns = [
    path('', views.FrontendView.as_view(), name="navigation_index"),
    path('navigation-link/', views.navigation_list, name="navigation_list"),
    path('navigation-box/', views.navigation_box, name="navigation_box"),
]