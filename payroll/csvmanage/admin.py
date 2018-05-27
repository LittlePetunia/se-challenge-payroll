from django.contrib import admin
from models import Report, Payroll, Payroll_Report
# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id',)

class PayrollAdmin(admin.ModelAdmin):
    list_display = ('id','date','hours_worked','employee_id','job_group','report_id')


class Payroll_ReportAdmin(admin.ModelAdmin):
    list_display = ('id','employee_id','period','period_start_date_ts','amount')

admin.site.register(Report, ReportAdmin) 
admin.site.register(Payroll, PayrollAdmin) 
admin.site.register(Payroll_Report, Payroll_ReportAdmin)