from django.forms import ModelForm
from main.models import *

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