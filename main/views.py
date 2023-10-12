from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    groups = Group.objects.all()

    context = {
        "groups": groups,
    }
    return render (request, "main/index.html", context)


def employees(request, groupId):
    group = Group.objects.get(id=groupId)
    employees = group.employees.all()

    for employee in employees:
        employee_last_year = employee.years.last()
        employee_last_month = employee.months.last()

    context = {
        "group": group,
        "employees": employees,
        "employee_last_year": employee_last_year,
        "employee_last_month": employee_last_month,
    }
    return render(request, "main/pages/employees.html", context)



def profile(request, groupId, employeeId, yearId, monthId):
    group = Group.objects.get(id=groupId)
    employee = group.employees.get(id=employeeId)
    year = employee.years.get(id=yearId)
    month = year.months.get(id=monthId)
    employee_days = month.days.all()

    context = {
        "group": group,
        "employee": employee,
        "year": year,
        "month": month,
        "employee_days": employee_days,
    }
    return render(request, "main/pages/profile.html", context)

