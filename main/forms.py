from django.forms import ModelForm
from main.models import *

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

class YearForm(ModelForm):
    class Meta:
        model = Year
        fields = "__all__"



class MonthForm(ModelForm):
    class Meta:
        model = Month
        fields = "__all__"



class DayForm(ModelForm):
    class Meta:
        model = Day
        fields = "__all__"