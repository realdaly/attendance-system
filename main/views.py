from django.shortcuts import render, redirect
from django.http import JsonResponse

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
    media_path = request.build_absolute_uri("/media/")
    group = Group.objects.get(id=groupId)
    employees = group.employees.all()
    employee_last_year = None
    employee_last_month = None

    for employee in employees:
        employee_last_year = employee.years.first()
        if employee_last_year:
            employee_last_month = employee_last_year.months.first()
        else:
            employee_last_year = None
            employee_last_month = None
            

    context = {
        "media_path": media_path,
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
def addGroup(request):
    if request.method == "POST":
        form = GroupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:index")
        else:
            return redirect("main:index")
        

def addEmployee(request, groupId):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            print(form.errors)
            return redirect("main:index")


def addYear(request, groupId):
    if request.method == "POST":
        form = YearForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            return redirect("main:index")
        


def addMonth(request, groupId, employeeId, yearId, monthId):
    if request.method == "POST":
        form = MonthForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:profile", groupId, employeeId, yearId, monthId)
        else:
            return redirect("main:index")
        


def addDay(request, groupId, employeeId, yearId, monthId):
    if request.method == "POST":
        form = DayForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:profile", groupId, employeeId, yearId, monthId)
        else:
            print(form.errors)
            return redirect("main:index")
            


def initMonth(request, groupId):
    if request.method == "POST":
        form = MonthForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            return redirect("main:index")
        

#  ---------------------------------------- UPDATE ----------------------------------------
def updateGroup(request, groupId):
    if request.method == "POST":
        group = Group.objects.get(id=groupId)
        form = GroupForm(request.POST, instance=group)

        if form.is_valid():
            form.save()
            return redirect("main:index")
        else:
            return redirect("main:index")
        
        
        
def updateEmployee(request, groupId, employeeId):
    if request.method == "POST":
        employee = Employee.objects.get(id=employeeId)
        form = EmployeeForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            form.save()
            return redirect("main:employees", groupId)
        else:
            print(form.errors)
            return redirect("main:index")
        


def updateYear(request, groupId, yearId, employeeId, currentYearId, currentMonthId):
    if request.method == "POST":
        year = Year.objects.get(id=yearId)
        form = YearForm(request.POST, instance=year)

        if form.is_valid():
            form.save()
            return redirect("main:profile", groupId, employeeId, currentYearId, currentMonthId)
        else:
            return redirect("main:index")
        


def updateMonth(request, groupId, monthId, employeeId, currentYearId, currentMonthId):
    if request.method == "POST":
        month = Month.objects.get(id=monthId)
        form = MonthForm(request.POST, instance=month)

        if form.is_valid():
            form.save()
            return redirect("main:profile", groupId, employeeId, currentYearId, currentMonthId)
        else:
            return redirect("main:index")
        

#  ---------------------------------------- DELETE ----------------------------------------
def deleteGroup(request, groupId):
    if request.method == "POST":
        group = Group.objects.get(id=groupId)
        group.delete()
        return redirect("main:index")
    


def deleteEmployee(request, groupId, employeeId):
    if request.method == "POST":
        employee = Employee.objects.get(id=employeeId)
        employee.delete()
        return redirect("main:employees", groupId)
    


def deleteYear(request, groupId, yearId):
    if request.method == "POST":
        year = Year.objects.get(id=yearId)
        year.delete()
        return redirect("main:employees", groupId)
    
    
def deleteMonth(request, groupId, monthId):
    if request.method == "POST":
        month = Month.objects.get(id=monthId)
        month.delete()
        return redirect("main:employees", groupId)