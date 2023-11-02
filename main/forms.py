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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the fields as not required and provide a default value
        self.fields['exit_hour'].required = False
        self.fields['exit_minute'].required = False
        self.fields['enter_hour'].required = False
        self.fields['enter_minute'].required = False
        self.fields['exit_hour'].widget.attrs['value'] = 0
        self.fields['exit_minute'].widget.attrs['value'] = 0
        self.fields['enter_hour'].widget.attrs['value'] = 0
        self.fields['enter_minute'].widget.attrs['value'] = 0