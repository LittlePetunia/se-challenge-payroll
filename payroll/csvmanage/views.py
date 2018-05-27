from models import Report, Payroll, Payroll_Report

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json, calendar
from datetime import datetime


def index(request):
    return render_to_response('csvmanage/index.html')


def get_current_report(request):
    '''
    Send response with all payroll report objects.
    '''
    response_data = list(Payroll_Report.objects.values())
    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


@csrf_exempt
def upload_csv(request, report_id):
    '''
    Take data (a list of payroll object in json format) sent by request.
    Create the Report object with report_id.
    If the report_id already in Report table, send error message.
    Else:
        Create Payroll objects for each object in data.
        Create Payroll_Report.
    '''
    report_count = Report.objects.filter(report_id=report_id).count()
    if report_count == 0: #report with report_id doesn't exist
        data = json.loads(request.body)
        # create a new Report
        new_report = Report(report_id=report_id)
        new_report.save()

        for obj in data:
            temp_date = [int(t) for t in obj['date'].split('/')]
            (day, month, year) = (temp_date[0], temp_date[1],
                                  temp_date[2])
            date = datetime(year=year, month=month, day=day)
            # create a Payroll for the current obj
            payroll = Payroll(date=date,
                              hours_worked=float(obj['hours worked']),
                              employee_id=int(obj['employee id']),
                              job_group=obj['job group'],
                              report_id=report_id)
            # 1 -> 1st half month, 16 -> 2nd half month
            start_day = (1 if day <= 15 else 16) 
            # get the end day of the given month 
            end_day = (15 if day <= 15 else calendar.monthrange(year,
                       month)[1])
            start_date_ts = 10000 * year + 100 * month + start_day

            # group A $20/h, group B $30/h
            if payroll.job_group == 'A':
                amount = 20 * payroll.hours_worked
            else:
                amount = 30 * payroll.hours_worked

            #check if the report with same pay period already existed
            payroll_report = \
                Payroll_Report.objects.filter(employee_id=payroll.employee_id,
                    period_start_date_ts=start_date_ts)

            if not payroll_report:
                # if report does not exists, create a new report
                period = str(start_day) + '/' + str(month) + '/' \
                    + str(year) + ' - ' + str(end_day) + '/' \
                    + str(month) + '/' + str(year)
                payroll_report = \
                    Payroll_Report(employee_id=payroll.employee_id,
                                   period_start_date_ts=start_date_ts,
                                   period=period, amount=amount)
            else:
                # if report exists, increment the amount of money
                payroll_report = payroll_report[0]
                payroll_report.amount += amount
            payroll_report.save()
            payroll.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    else:
        return HttpResponse(json.dumps({'status': 'error',
                            'error_message': 'This report is already been uploaded before'
                            }))
