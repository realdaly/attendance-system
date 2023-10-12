from django.db import models
from django.db.models import F

class Image(models.Model):
    image = models.ImageField(upload_to="images", blank=False)
    title = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        if not self.title:
            filename = self.image.name
            self.title = filename.split('.')[0]
        
        super().save(*args, **kwargs)

class Group(models.Model):
    title = models.CharField(max_length=255)
    required_hours = models.PositiveIntegerField(default=0)
    required_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    



class Employee(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="employees", null=True, blank=True)
    main_img = main_img = models.ForeignKey(Image, default=0, on_delete=models.PROTECT, related_name="employees")
    order = models.PositiveIntegerField(default=0)  # To specify the order of employees

    def __str__(self):
        return self.name

    


class Year(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="years", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="years")
    title = models.CharField(max_length=4)  # For example, "2023"
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def update_more_less(self):
        # Calculate the difference between more and less hours and minutes
        more_hours = self.months.aggregate(models.Sum('more_hours'))['more_hours__sum'] or 0
        more_minutes = self.months.aggregate(models.Sum('more_minutes'))['more_minutes__sum'] or 0
        less_hours = self.months.aggregate(models.Sum('less_hours'))['less_hours__sum'] or 0
        less_minutes = self.months.aggregate(models.Sum('less_minutes'))['less_minutes__sum'] or 0

        # Convert each 60 minutes to 1 hour
        if less_minutes >= 60:
            less_hours = less_hours + less_minutes / 60
            less_minutes = less_minutes % 60

        if more_minutes >= 60:
            more_hours = more_hours + more_minutes / 60
            more_minutes = more_minutes % 60

        result_hours = more_hours - less_hours
        result_minutes = more_minutes - less_minutes

        # Update more and less hours and minutes based on the result
        if result_hours < 0:
            self.less_hours = abs(result_hours)
            self.more_hours = 0
        elif result_hours > 0:
            self.more_hours = result_hours
            self.less_hours = 0
        else:
            self.more_hours = 0
            self.more_minutes = 0

        if result_minutes < 0:
            self.less_minutes = abs(result_minutes)
            self.more_minutes = 0
        elif result_minutes > 0:
            self.more_minutes = result_minutes
            self.less_minutes = 0
        else:
            self.more_minutes = 0
            self.less_minutes = 0

        self.save()
    
    
    


class Month(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="months", null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="months")
    title = models.CharField(max_length=255)
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
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

        # Convert each 60 minutes to 1 hour
        if less_minutes >= 60:
            less_hours = less_hours + less_minutes / 60
            less_minutes = less_minutes % 60

        if more_minutes >= 60:
            more_hours = more_hours + more_minutes / 60
            more_minutes = more_minutes % 60

        result_hours = more_hours - less_hours
        result_minutes = more_minutes - less_minutes

        # Update more and less hours and minutes based on the result
        if result_hours < 0:
            self.less_hours = abs(result_hours)
            self.more_hours = 0
        elif result_hours > 0:
            self.more_hours = result_hours
            self.less_hours = 0
        else:
            self.more_hours = 0
            self.more_minutes = 0

        if result_minutes < 0:
            self.less_minutes = abs(result_minutes)
            self.more_minutes = 0
        elif result_minutes > 0:
            self.more_minutes = result_minutes
            self.less_minutes = 0
        else:
            self.more_minutes = 0
            self.less_minutes = 0

        self.save()
    
    




class Day(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="days")
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="days")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="days")
    title = models.CharField(max_length=255, null=True, blank=True)
    required_hours = models.PositiveIntegerField()
    required_minutes = models.PositiveIntegerField()
    attend_hour = models.PositiveIntegerField()
    attend_minute = models.PositiveIntegerField()
    leave_hour = models.PositiveIntegerField()
    leave_minute = models.PositiveIntegerField()
    more_hours = models.PositiveIntegerField(default=0)
    more_minutes = models.PositiveIntegerField(default=0)
    less_hours = models.PositiveIntegerField(default=0)
    less_minutes = models.PositiveIntegerField(default=0)
    total_hours = models.IntegerField(default=0)
    total_minutes = models.IntegerField(default=0)
    note = models.TextField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.month.title} {self.year.title}"
    
    def update_month_and_year(self):
        # Update related Month and Year
        self.month.update_more_less()
        self.year.update_more_less()

    def save(self, *args, **kwargs):
        # Calculate the total minutes worked
        total_minutes = (self.leave_hour * 60 + self.leave_minute) - (self.attend_hour * 60 + self.attend_minute)

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