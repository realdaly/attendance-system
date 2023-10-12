from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:groupId>/employees/", views.employees, name="employees"),
    path("<str:groupId>/profile/<str:employeeId>/<str:yearId>/<str:monthId>/", views.profile, name="profile")
]