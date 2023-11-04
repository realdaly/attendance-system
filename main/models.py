from django.db import models
from django.db.models import F


class Group(models.Model):
    title = models.CharField(max_length=255, default="مجموعة بدون عنوان")
    required_hours = models.PositiveIntegerField(default=0)
    required_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    



class Employee(models.Model):
    name = models.CharField(max_length=255, default="موظف بدون أسم")
    image = models.ImageField(upload_to="images", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    


class Year(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="years", null=True, blank=True)
    title = models.CharField(max_length=10, default="سنة بدون عنوان")
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']

    def update_more_less(self):
        self.more_hours = 0
        self.more_minutes = 0
        self.less_hours = 0
        self.less_minutes = 0


        # Calculate the difference between more and less hours and minutes
        more_hours = self.months.aggregate(models.Sum('more_hours'))['more_hours__sum'] or 0
        more_minutes = self.months.aggregate(models.Sum('more_minutes'))['more_minutes__sum'] or 0
        less_hours = self.months.aggregate(models.Sum('less_hours'))['less_hours__sum'] or 0
        less_minutes = self.months.aggregate(models.Sum('less_minutes'))['less_minutes__sum'] or 0

        # Convert all time to minutes
        result_more = more_hours * 60 + more_minutes
        result_less = less_hours * 60 + less_minutes

        # Finding the difference between more and less and specifiying how much more and less according to that
        final_result = result_more - result_less

        if final_result < 0:
            self.less_hours = abs(final_result) / 60
            self.less_minutes = abs(final_result) % 60
            self.more_hours = 0
            self.more_minutes = 0

        elif final_result > 0:
            self.more_hours = abs(final_result) / 60
            self.more_minutes = abs(final_result) % 60
            self.less_hours = 0
            self.less_minutes = 0
        else:
            self.more_hours = 0
            self.more_minutes = 0
            self.less_hours = 0
            self.less_minutes = 0

        self.save()
    
    
    


class Month(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="months", null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="months")
    title = models.CharField(max_length=50, default="شهر في السنة")
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']
    
    def update_more_less(self):
        self.more_hours = 0
        self.more_minutes = 0
        self.less_hours = 0
        self.less_minutes = 0
        
        
        # Calculate the difference between more and less hours and minutes
        more_hours = self.days.aggregate(models.Sum('more_hours'))['more_hours__sum'] or 0
        more_minutes = self.days.aggregate(models.Sum('more_minutes'))['more_minutes__sum'] or 0
        less_hours = self.days.aggregate(models.Sum('less_hours'))['less_hours__sum'] or 0
        less_minutes = self.days.aggregate(models.Sum('less_minutes'))['less_minutes__sum'] or 0

        # Convert all time to minutes
        result_more = more_hours * 60 + more_minutes
        result_less = less_hours * 60 + less_minutes

        # Finding the difference between more and less and specifiying how much more and less according to that
        final_result = result_more - result_less

        if final_result < 0:
            self.less_hours = abs(final_result) / 60
            self.less_minutes = abs(final_result) % 60
            self.more_hours = 0
            self.more_minutes = 0

        elif final_result > 0:
            self.more_hours = abs(final_result) / 60
            self.more_minutes = abs(final_result) % 60
            self.less_hours = 0
            self.less_minutes = 0
        else:
            self.more_hours = 0
            self.more_minutes = 0
            self.less_hours = 0
            self.less_minutes = 0

        self.save()
    
    




class Day(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="days")
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="days")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="days")
    title = models.CharField(max_length=50, default="يوم في الشهر", null=True, blank=True)
    date_month = models.CharField(max_length=50, default=0, null=True, blank=True)
    date_day = models.CharField(max_length=50, default=0, null=True, blank=True)
    required_hours = models.PositiveIntegerField()
    required_minutes = models.PositiveIntegerField()
    attend_hour = models.PositiveIntegerField(null=True, blank=True)
    attend_minute = models.PositiveIntegerField(null=True, blank=True)
    leave_hour = models.PositiveIntegerField(null=True, blank=True)
    leave_minute = models.PositiveIntegerField(null=True, blank=True)
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)
    total_hours = models.IntegerField(default=0)
    total_minutes = models.IntegerField(default=0)
    exit_hour = models.PositiveIntegerField(null=True, blank=True)
    exit_minute = models.PositiveIntegerField(null=True, blank=True)
    enter_hour = models.PositiveIntegerField(null=True, blank=True)
    enter_minute = models.PositiveIntegerField(null=True, blank=True)
    time_off = models.BooleanField(default=False)
    note = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.month.title} {self.year.title}"
    
    class Meta:
        ordering = ['-id']
    
    def update_month_and_year(self):
        # Update related Month and Year
        self.month.update_more_less()
        self.year.update_more_less()

    def save(self, *args, **kwargs):
        if self.time_off:
            pass
        
        total_implicit_minutes = 0

        if self.exit_hour or self.enter_hour:
            # Get implicit exit and enter times in minutes
            total_implicit_minutes =  (self.enter_hour * 60 + self.enter_minute) - (self.exit_hour * 60 + self.exit_minute)

        if(self.time_off):
            self.attend_hour = 0
            self.attend_minute = 0
            self.leave_hour = 0
            self.leave_minute = 0
            self.more_hours = 0
            self.more_minutes = 0
            self.less_hours = 0
            self.less_minutes = 0
            self.total_hours = 0
            self.total_minutes = 0

        else:
            # Calculate the total minutes worked
            total_minutes = (self.leave_hour * 60 + self.leave_minute) - (self.attend_hour * 60 + self.attend_minute) - total_implicit_minutes

            # Calculate the total hours and total minutes
            self.total_hours = total_minutes // 60
            self.total_minutes = total_minutes % 60

            # Calculate the difference between total time and required time
            required_minutes = (self.required_hours * 60) + self.required_minutes

            if total_minutes > required_minutes:
                self.more_hours = (total_minutes - required_minutes) // 60
                self.more_minutes = (total_minutes - required_minutes) % 60
                self.less_hours = 0
                self.less_minutes = 0
            elif total_minutes < required_minutes:
                self.less_hours = (required_minutes - total_minutes) // 60
                self.less_minutes = (required_minutes - total_minutes) % 60
                self.more_hours = 0
                self.more_minutes = 0
            else:
                self.less_hours = 0
                self.less_minutes = 0
                self.more_hours = 0
                self.more_minutes = 0

        super().save(*args, **kwargs)
        self.update_month_and_year()

    
    def delete(self, *args, **kwargs):

        super().delete(*args, **kwargs)
        self.update_month_and_year()