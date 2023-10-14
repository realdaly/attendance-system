from django.shortcuts import render, redirect

from .models import *
from .forms import *

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
        employee_last_year = employee.years.first()
        if employee_last_year:
            employee_last_month = employee_last_year.months.first()
        else:
            employee_last_year = None
            employee_last_month = None
            

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
    current_year = employee.years.get(id=yearId)
    current_month = current_year.months.get(id=monthId)
    employee_days = current_month.days.all()


    context = {
        "group": group,
        "employee": employee,
        "current_year": current_year,
        "current_month": current_month,
        "employee_days": employee_days,
    }
    return render(request, "main/pages/profile.html", context)

 

#  ---------------------------------------- ADD ----------------------------------------
def addYear(request, groupId):
    if request.method == "POST":
        employee = request.POST["employee"]
        title = request.POST["title"]
        more_hours = request.POST["more_hours"]
        more_minutes = request.POST["more_minutes"]
        less_hours = request.POST["less_hours"]
        less_minutes = request.POST["less_minutes"]

        data = {
            "employee": employee,
            "title": title,
            "more_hours": more_hours,
            "more_minutes": more_minutes,
            "less_hours": less_hours,
            "less_minutes": less_minutes,
        }

        form = YearForm(data)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            return redirect("main:index")
        


def addMonth(request, groupId):
    if request.method == "POST":
        employee = request.POST["employee"]
        year = request.POST["year"]
        title = request.POST["title"]
        more_hours = request.POST["more_hours"]
        more_minutes = request.POST["more_minutes"]
        less_hours = request.POST["less_hours"]
        less_minutes = request.POST["less_minutes"]

        data = {
            "employee": employee,
            "year": year,
            "title": title,
            "more_hours": more_hours,
            "more_minutes": more_minutes,
            "less_hours": less_hours,
            "less_minutes": less_minutes,
        }

        form = MonthForm(data)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            return redirect("main:index")
        


def addDay(request, groupId, employeeId, yearId, monthId):
    if request.method == "POST":
        employee = request.POST["employee"]
        month = request.POST["month"]
        year = request.POST["year"]
        title = request.POST["title"]
        required_hours = request.POST["required_hours"]
        required_minutes = request.POST["required_minutes"]
        attend_hour = request.POST["attend_hour"]
        attend_minute = request.POST["attend_minute"]
        leave_hour = request.POST["leave_hour"]
        leave_minute = request.POST["leave_minute"]
        more_hours = request.POST["more_hours"]
        more_minutes = request.POST["more_minutes"]
        less_hours = request.POST["less_hours"]
        less_minutes = request.POST["less_minutes"]
        total_hours = request.POST["total_hours"]
        total_minutes = request.POST["total_minutes"]
        note = request.POST["note"]

        data = {
            "employee": employee,
            "month": month,
            "year": year,
            "title": title,
            "required_hours": required_hours,
            "required_minutes": required_minutes,
            "attend_hour": attend_hour,
            "attend_minute": attend_minute,
            "leave_hour": leave_hour,
            "leave_minute": leave_minute,
            "more_hours": more_hours,
            "more_minutes": more_minutes,
            "less_hours": less_hours,
            "less_minutes": less_minutes,
            "total_hours": total_hours,
            "total_minutes": total_minutes,
            "note": note,
        }

        form = DayForm(data)

        if form.is_valid():
            form.save()
            return redirect("main:profile", groupId, employeeId, yearId, monthId)
        else:
            print(form.errors)
            return redirect("main:index")
            

