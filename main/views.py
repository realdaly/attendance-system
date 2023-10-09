from django.shortcuts import render

# Create your views here.
def index(request):

    context = {}
    return render (request, "main/index.html", context)


def employees(request):

    context = {}
    return render(request, "main/pages/employees.html", context)