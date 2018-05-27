from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Report(models.Model):
    report_id = models.PositiveIntegerField()

class Payroll(models.Model):
    date = models.DateField()
    hours_worked = models.FloatField()
    employee_id = models.PositiveIntegerField()
    job_group = models.CharField(max_length=100)
    report_id = models.PositiveIntegerField()

class Payroll_Report(models.Model):
    employee_id = models.PositiveIntegerField()
    period = models.CharField(max_length=25)
    period_start_date_ts = models.PositiveIntegerField()
    amount = models.PositiveIntegerField() 

    class Meta:
        ordering = ['employee_id', 'period_start_date_ts']