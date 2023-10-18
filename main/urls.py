from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    #READ
    path("", views.index, name="index"),
    path("<str:groupId>/employees/", views.employees, name="employees"),
    path("<str:groupId>/profile/<str:employeeId>/<str:yearId>/<str:monthId>/", views.profile, name="profile"),

    # ADD
    path("addGroup/", views.addGroup, name="addGroup"),
    path("<str:groupId>/addEmployee/", views.addEmployee, name="addEmployee"),
    path("<str:groupId>/addYear/", views.addYear, name="addYear"),
    path("<str:groupId>/initMonth/", views.initMonth, name="initMonth"), 
    path("<str:groupId>/addMonth/<str:employeeId>/<str:yearId>/<str:monthId>/", views.addMonth, name="addMonth"),
    path("<str:groupId>/addDay/<str:employeeId>/<str:yearId>/<str:monthId>/", views.addDay, name="addDay"),

    # UPDATE
    path("updateGroup/<str:groupId>", views.updateGroup, name="updateGroup"),
    path("<str:groupId>/<str:employeeId>/updateEmployee/", views.updateEmployee, name="updateEmployee"),
    path("<str:groupId>/<str:yearId>/updateYear/<str:employeeId>/<str:currentYearId>/<str:currentMonthId>/", views.updateYear, name="updateYear"),
    path("<str:groupId>/<str:monthId>/updateMonth/<str:employeeId>/<str:currentYearId>/<str:currentMonthId>/", views.updateMonth, name="updateMonth"),
    path("<str:groupId>/<str:dayId>/updateDay/<str:employeeId>/<str:currentYearId>/<str:currentMonthId>/", views.updateDay, name="updateDay"),

    # DELETE
    path("deleteGroup/<str:groupId>", views.deleteGroup, name="deleteGroup"),
    path("<str:groupId>/<str:employeeId>/deleteEmployee/", views.deleteEmployee, name="deleteEmployee"),
    path("<str:groupId>/<str:yearId>/deleteYear/", views.deleteYear, name="deleteYear"),
    path("<str:groupId>/<str:monthId>/deleteMonth/", views.deleteMonth, name="deleteMonth"),
    path("<str:groupId>/<str:dayId>/deleteDay/<str:employeeId>/<str:currentYearId>/<str:currentMonthId>/", views.deleteDay, name="deleteDay"),
]