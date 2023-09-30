from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import date
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
import calendar
from django.db.models import Sum
from datetime import timedelta
import csv
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import inflect
from django.contrib import messages
from .helpers import send_forget_password_mail
import uuid


# Create your views here.

def HomePage(request):
    if 'login_status' in request.COOKIES and 'username' in request.COOKIES:
        context = {
            'username': request.COOKIES.get('username'),
            'login_status' : request.COOKIES.get('login_status'),
        }
        return redirect('markAttend')
    elif 'login_status' in request.COOKIES and 'username' in request.COOKIES:
        context = {
            'username': request.COOKIES.get('username'),
            'login_status' : request.COOKIES.get('login_status'),
        }
        return redirect('allEmployeeDetails')
    else :
        return render(request, 'index.html')


def register(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        ei = request.POST['emailid']
        pwd = request.POST['pwd1']
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=ei, password=pwd)
            EmployeeDetail.objects.create(user=user,empcode=ec)
            error = "no"
        except:
            error = "yes"
    return render(request,'registration.html',locals())

from django.http import HttpResponse

def employeeLogin(request):
    error = ""

    if request.method == "POST":
        u = request.POST['emailid']
        pwd = request.POST['password']
        user = authenticate(username=u, password=pwd)
        if user is not None:
            login(request, user)
            error = "no"
            response = render(request, 'employeeLogin.html', locals())
            response.set_cookie('username', u, max_age=3600)  # Set username cookie with a 1-hour expiration
            response.set_cookie('login_status', 'True', max_age=3600)  # Set login_status cookie
            return response  # Return the response after setting cookies
        else:
            error = "yes"
    
    return render(request, 'employeeLogin.html', locals())


def employeeHome(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    emp = EmployeeDetail.objects.get(user=request.user)
    return render(request, 'employeeHome.html',locals())


def viewProfile(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if not employee.pfno:
        employee.pfno = "Not Applicable"
    if not employee.uan:
        employee.uan = "Not Applicable"
    if not employee.esicip:
        employee.esicip = "Not Applicable"
    return render(request, 'viewProfile.html', locals())

def Logout(request):
    logout(request)
    return redirect('HomePage')


def empChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    error = ""
    user = request.user
    if request.method == "POST":
        cp = request.POST['currentpwd']
        newp = request.POST['newpwd']
        try:
            if user.check_password(cp):
                user.set_password(newp)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    
    return render(request, 'employeeChangePwd.html',locals())

def adminLogin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_superuser:
                login(request,user)
                error = "no"
                response = render(request, 'adminLogin.html', locals())
                response.set_cookie('username', u, max_age=3600)  # Set username cookie with a 1-hour expiration
                response.set_cookie('login_status', 'True', max_age=3600)  # Set login_status cookie
                return response  # Return the response after setting cookies
            else :
                error = "yes"
        except:
            error = "yes"
        
    return render(request, 'adminLogin.html', locals())


def adminHome(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    return render(request, 'adminHome.html')


def adminChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    error = ""
    user = request.user
    if request.method == "POST":
        cp = request.POST['currentpwd']
        newp = request.POST['newpwd']
        try:
            if user.check_password(cp):
                user.set_password(newp)
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    
    return render(request, 'adminChangePwd.html',locals())


def allEmployeeDetails(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    employee = EmployeeDetail.objects.all()
    return render(request, 'allEmployeeDetails.html',locals())


def attendanceReport(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    emp = Attend.objects.all()
    cnt = emp.count()
    print(cnt)
    return render(request, 'allEmpAttendance.html',{'emp':emp,'cnt':cnt})

def viewEmployeeAttendance(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    emp1 = Attendance.objects.filter(employee = request.user)
    cnt = emp1.count()
    emp = Attendance.objects.get(employee = request.user)
    return render(request, 'viewEmployeeAttendance.html',locals())

'''
def approveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()
    return redirect('viewLeaveApplication')

def disapproveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()
    return redirect('viewLeaveApplication')
'''
def viewLeaveApplication(request):
    user = request.user
    # Get the specific leave application if application_id is provided

    managed_leave_apps = ApplyForLeave.objects.filter(man=user).order_by('-start_date')
    context = {
        'managed_leave_apps':managed_leave_apps,
    }

    return render(request, 'viewLeaveApplication.html', context)


def viewEmpLeaveApplication(request):
    user = request.user
    employee = ApplyForLeave.objects.filter(user=user).order_by('-start_date')
    return render(request, 'viewEmpLeaveApplication.html',locals())



def markAttend(request):
    man = 0
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    attendance_date = date.today()
    flag = 0
    if attendance_date.weekday() == 6:
        flag=1
    attendance = Attend.objects.filter(user=user, date = attendance_date).first()
    if attendance :
        pass
    else:
        attendance = Attend.objects.create(user=user, date=attendance_date, is_present=0)
    emp = EmployeeDetail.objects.get(user=user)
    employee_attendance = []
    absent_count = 0
    present_count = 0
    on_leave_count = 0
    attendance_status = 0 if attendance is None else attendance.is_present
    if attendance_status == 0:
        absent_count +=1
    elif attendance_status == 1:
        present_count+=1
    elif attendance_status == 2:
        on_leave_count+=1
    employee_attendance.append({
        'employee':emp,
        'attendance':attendance_status
    })
    if emp.designation == "Manager":
        man = 1
        emps = EmployeeDetail.objects.filter(manage=user.username)
                # Create a list to store the is_present status of employees
        
        
        for e in emps:
            attendance_record = Attend.objects.filter(user=e.user, date=attendance_date).first()
            attendance_status = 0 if attendance_record is None else attendance_record.is_present
            if attendance_record:
                if attendance_record.is_present == 1:
                    present_count += 1
                elif attendance_record.is_present == 2:
                    on_leave_count += 1
            if attendance_record is None :
                absent_count +=1
    
            employee_attendance.append({
        'employee': e,
        'attendance': attendance_status
    })
        #print(employee_attendance)
        #print(absent_count)
        #print(on_leave_count)
        #print(present_count)
    else:
        man = 0
        pass
    return render(request,'markAttend.html',locals())

def updateAttendanceSummary(request):
    try:
        attendance_data = AttendanceSummary.objects.get(user=request.user)
        cnt = 1
    except:
        attendance_data = AttendanceSummary.objects.filter(user=request.user)
        cnt = 2
    return render(request, 'attendSummary.html',locals())

def markA(request):
    attendM = Attend.objects.get(user=request.user, date=str(date.today()))
    dat = date.today()
    # Get the selected month and year from the attendance_date
    selected_month = dat.month
    selected_year = dat.year

    # Update or create the attendance summary
    summary, created = AttendanceSummary.objects.get_or_create(
        user=request.user,
        month=selected_month,
        year=selected_year,
    )
    attendM.is_present = 1
    summary.days_present +=1
    summary.days_total = calendar.monthrange(selected_year, selected_month)[1]
    # Get the calendar for the specified year and month
    cal = calendar.monthcalendar(selected_year, selected_month)
    # Count the number of Sundays (which are represented by weekday 6)
    sundays = sum(1 for week in cal if week[calendar.SUNDAY] != 0)
    summary.sundays = sundays
    attendM.save()
    summary.save()
    return redirect('markAttend')

# to see attendance report of particular user
def viewAttendance(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    user = request.user
    attendance_data = AttendanceSummary.objects.filter(user=user)
    return render(request, 'viewAttendance.html',locals())

# to see attendance report of all the users
def viewAttendanceReport(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    attendance_data = AttendanceSummary.objects.all()
    cnt = attendance_data.count()
    return render(request, 'viewAttendanceReport.html', locals())


def pS(request):
    if request.method == "POST":
        temp = 0
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        flag = 0
        days_total = 30
        emp = EmployeeDetail.objects.get(user=request.user)
        # Assuming selected_month and selected_year are integers
        month_to_int = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}
        selected_month_int = month_to_int.get(selected_month)
        s_year = 0
        e_year = 0
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        start_date = datetime(s_year, 4, 1)
        end_date = datetime(s_year, selected_month_int, 1)
        print(start_date)
        print(end_date)
        print(s_year)
        print(e_year)
        print(end_date)
        if s_year == int(selected_year):
            start_date = datetime(s_year, 4, 1)
            end_date = datetime(s_year, selected_month_int, 1)
            temp = 1
        if s_year != int(selected_year):
            start_date = datetime(s_year, 4, 1)
            end_date = datetime(e_year, selected_month_int, 1)
            temp = 2
        print(temp)
        if emp.emptype == 'Staff':
            try:
                staffCal = StaffSalaryCalculation.objects.get(empcode=emp.empcode,month=selected_month, year=selected_year)
                if staffCal:
                    flag = 1
                if temp == 1:
                    staffCal2 = StaffSalaryCalculation.objects.filter(
            empcode=emp.empcode,
            year=s_year,
            month_int__gte=start_date.month,
            month_int__lte=end_date.month
        )
                    print(staffCal2)
                elif temp == 2:
                    staffCal2_1 = StaffSalaryCalculation.objects.filter(
            empcode=emp.empcode,
            year=s_year,
            month_int__gte=start_date.month,
            month_int__lte=12)
                    staffCal2_2 = StaffSalaryCalculation.objects.filter(
            empcode=emp.empcode,
            year=e_year,
            month_int__gte=1,
            month_int__lte=end_date.month)
                    #print(staffCal2_1)
                    #print(staffCal2_2)
                staffCal2 = staffCal2_1.union(staffCal2_2)
                print(staffCal2)
                if staffCal:
                    p = inflect.engine()
                    bas = staffCal.basic_a
                    if 0 <= bas < 10**12 :
                        bas = "{:,.2f}".format(bas)
                    hra = staffCal.hra_a
                    if 0 <= hra < 10**12 :
                        hra = "{:,.2f}".format(hra)
                    speAll = staffCal.specialAll_a
                    if 0 <= speAll < 10**12 :
                        speAll = "{:,.2f}".format(speAll)
                    ince = staffCal.incentive
                    if 0 <= ince < 10**12 :
                        ince = "{:,.2f}".format(ince)
                    proTax = staffCal.professional_tax
                    if 0 <= proTax < 10**12 :
                        proTax = "{:,.2f}".format(proTax)
                    amt = staffCal.netSalary
                    if 0 <= amt < 10**12 :
                        amt = "{:,.2f}".format(amt)
                    oe = staffCal.others
                    if 0 <= oe < 10**12:
                        oe = "{:,.2f}".format(oe)
                    pf_ded = staffCal.pf_deduction
                    if 0 <= pf_ded < 10**12:
                        pf_ded = "{:,.2f}".format(pf_ded)
                    esic_ded = staffCal.esic_deduction
                    if 0 <= esic_ded < 10**12:
                        esic_ded = "{:,.2f}".format(esic_ded)
                    od = staffCal.other_deduction
                    if 0 <= od < 10**12:
                        od = "{:,.2f}".format(od)
                    gross_sal_a = staffCal.grossS_a
                    if 0 <= gross_sal_a < 10**12:
                        gross_sal_a = "{:,.2f}".format(gross_sal_a)
                    gross_ded = staffCal.gross_deduction
                    if 0 <= gross_ded < 10**12:
                        gross_ded = "{:,.2f}".format(gross_ded)
                    if 0 <= staffCal.netSalary < 10**12:
                        amount = p.number_to_words(staffCal.netSalary).replace(".0","")
                        if amount.endswith(" point zero"):
                            amount = amount[:-len(" point zero")]
                
                basic_a_all = 0.0
                hra_a_all = 0.0
                speAll_a_all = 0.0
                bonus_all = 0.0
                oe_all = 0.0
                pro_t_all = 0.0
                pf_ded_all = 0.0
                esic_ded_all = 0.0
                other_ded_all = 0.0
                gross_sal_a_all = 0.0
                gross_ded_all = 0.0
                for cal in staffCal2:
                    basic_a_all += cal.basic_a
                    hra_a_all += cal.hra_a
                    speAll_a_all += cal.specialAll_a
                    bonus_all += cal.incentive
                    oe_all += cal.others
                    pro_t_all += cal.professional_tax
                    pf_ded_all += cal.pf_deduction
                    esic_ded_all += cal.esic_deduction
                    other_ded_all += cal.other_deduction
                    gross_sal_a_all += cal.grossS_a
                    gross_ded_all += cal.gross_deduction
                if 0 <= basic_a_all < 10**12:
                    basic_a_all = "{:,.2f}".format(basic_a_all)
                if 0 <= hra_a_all < 10**12:
                    hra_a_all = "{:,.2f}".format(hra_a_all)
                if 0 <= speAll_a_all < 10**12:
                    speAll_a_all = "{:,.2f}".format(speAll_a_all)
                if 0 <= bonus_all < 10**12:
                    bonus_all = "{:,.2f}".format(bonus_all)
                if 0 <= oe_all < 10**12:
                    oe_all = "{:,.2f}".format(oe_all)
                if 0 <= pro_t_all < 10**12:
                    pro_t_all = "{:,.2f}".format(pro_t_all)
                if 0 <= pf_ded_all < 10**12:
                    pf_ded_all = "{:,.2f}".format(pf_ded_all)
                if 0 <= esic_ded_all < 10**12:
                    esic_ded_all = "{:,.2f}".format(esic_ded_all)
                if 0 <= other_ded_all < 10**12:
                    other_ded_all = "{:,.2f}".format(other_ded_all)
                if 0 <= gross_sal_a_all < 10**12:
                    gross_sal_a_all = "{:,.2f}".format(gross_sal_a_all)
                if 0 <= gross_ded_all < 10**12:
                    gross_ded_all = "{:,.2f}".format(gross_ded_all)                
                
            except :
                flag = 0
    return render(request, 'paySlip.html', locals())

def paySlip(request):
    if request.method == "POST":
        temp = 0
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        flag = ""
        days_total = 30
        emp = EmployeeDetail.objects.get(user=request.user)
        # Assuming selected_month and selected_year are integers
        month_to_int = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}
        selected_month_int = month_to_int.get(selected_month)
        s_year = 0
        e_year = 0
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        start_date = datetime(s_year, 4, 1)
        end_date = datetime(s_year, selected_month_int, 1)
        print(start_date)
        print(end_date)
        print(s_year)
        print(e_year)
        print(end_date)
        if s_year == int(selected_year):
            start_date = datetime(s_year, 4, 1)
            end_date = datetime(s_year, selected_month_int, 1)
            temp = 1
        if s_year != int(selected_year):
            start_date = datetime(s_year, 4, 1)
            end_date = datetime(e_year, selected_month_int, 1)
            temp = 2
        print(temp)
        if emp.emptype == 'Staff':
            try:
                staffCal = StaffSalaryCalculation.objects.get(empcode=emp.empcode,month=selected_month, year=selected_year)
                if staffCal:
                    flag = "no"
                    if temp == 1:
                        staffCal2 = StaffSalaryCalculation.objects.filter(
                        empcode=emp.empcode,
                        year=s_year,
                        month_int__gte=start_date.month,
                        month_int__lte=end_date.month
                        )
                
                        print(staffCal2)
                    elif temp == 2:
                        staffCal2_1 = StaffSalaryCalculation.objects.filter(
                        empcode=emp.empcode,
                        year=s_year,
                        month_int__gte=start_date.month,
                        month_int__lte=12)
                        staffCal2_2 = StaffSalaryCalculation.objects.filter(
                        empcode=emp.empcode,
                        year=e_year,
                        month_int__gte=1,
                        month_int__lte=end_date.month)
                    #print(staffCal2_1)
                    #print(staffCal2_2)
                        staffCal2 = staffCal2_1.union(staffCal2_2)
                        print(staffCal2)
                    p = inflect.engine()
                    bas = staffCal.basic_a
                    if 0 <= bas < 10**12 :
                        bas = "{:,.2f}".format(bas)
                    hra = staffCal.hra_a
                    if 0 <= hra < 10**12 :
                        hra = "{:,.2f}".format(hra)
                    speAll = staffCal.specialAll_a
                    if 0 <= speAll < 10**12 :
                        speAll = "{:,.2f}".format(speAll)
                    ince = staffCal.incentive
                    if 0 <= ince < 10**12 :
                        ince = "{:,.2f}".format(ince)
                    proTax = staffCal.professional_tax
                    if 0 <= proTax < 10**12 :
                        proTax = "{:,.2f}".format(proTax)
                    amt = staffCal.netSalary
                    if 0 <= amt < 10**12 :
                        amt = "{:,.2f}".format(amt)
                    oe = staffCal.others
                    if 0 <= oe < 10**12:
                        oe = "{:,.2f}".format(oe)
                    pf_ded = staffCal.pf_deduction
                    if 0 <= pf_ded < 10**12:
                        pf_ded = "{:,.2f}".format(pf_ded)
                    esic_ded = staffCal.esic_deduction
                    if 0 <= esic_ded < 10**12:
                        esic_ded = "{:,.2f}".format(esic_ded)
                    od = staffCal.other_deduction
                    if 0 <= od < 10**12:
                        od = "{:,.2f}".format(od)
                    gross_sal_a = staffCal.grossS_a
                    if 0 <= gross_sal_a < 10**12:
                        gross_sal_a = "{:,.2f}".format(gross_sal_a)
                    gross_ded = staffCal.gross_deduction
                    if 0 <= gross_ded < 10**12:
                        gross_ded = "{:,.2f}".format(gross_ded)
                    if 0 <= staffCal.netSalary < 10**12:
                        amount = p.number_to_words(staffCal.netSalary).replace(".0","")
                        if amount.endswith(" point zero"):
                            amount = amount[:-len(" point zero")]
                    basic_a_all = 0.0
                    hra_a_all = 0.0
                    speAll_a_all = 0.0
                    bonus_all = 0.0
                    oe_all = 0.0
                    pro_t_all = 0.0
                    pf_ded_all = 0.0
                    esic_ded_all = 0.0
                    other_ded_all = 0.0
                    gross_sal_a_all = 0.0
                    gross_ded_all = 0.0
                    for cal in staffCal2:
                        basic_a_all += cal.basic_a
                        hra_a_all += cal.hra_a
                        speAll_a_all += cal.specialAll_a
                        bonus_all += cal.incentive
                        oe_all += cal.others
                        pro_t_all += cal.professional_tax
                        pf_ded_all += cal.pf_deduction
                        esic_ded_all += cal.esic_deduction
                        other_ded_all += cal.other_deduction
                        gross_sal_a_all += cal.grossS_a
                        gross_ded_all += cal.gross_deduction
                    if 0 <= basic_a_all < 10**12:
                        basic_a_all = "{:,.2f}".format(basic_a_all)
                    if 0 <= hra_a_all < 10**12:
                        hra_a_all = "{:,.2f}".format(hra_a_all)
                    if 0 <= speAll_a_all < 10**12:
                        speAll_a_all = "{:,.2f}".format(speAll_a_all)
                    if 0 <= bonus_all < 10**12:
                        bonus_all = "{:,.2f}".format(bonus_all)
                    if 0 <= oe_all < 10**12:
                        oe_all = "{:,.2f}".format(oe_all)
                    if 0 <= pro_t_all < 10**12:
                        pro_t_all = "{:,.2f}".format(pro_t_all)
                    if 0 <= pf_ded_all < 10**12:
                        pf_ded_all = "{:,.2f}".format(pf_ded_all)
                    if 0 <= esic_ded_all < 10**12:
                        esic_ded_all = "{:,.2f}".format(esic_ded_all)
                    if 0 <= other_ded_all < 10**12:
                        other_ded_all = "{:,.2f}".format(other_ded_all)
                    if 0 <= gross_sal_a_all < 10**12:
                        gross_sal_a_all = "{:,.2f}".format(gross_sal_a_all)
                    if 0 <= gross_ded_all < 10**12:
                        gross_ded_all = "{:,.2f}".format(gross_ded_all)                
                
            except :
                pass
        elif emp.emptype == 'Professional':
            try:
                profCal = ProfessionalSalaryCal.objects.get(empcode=emp.empcode, month=selected_month, year=selected_year)
                print(profCal)
                if profCal:
                    flag = "no"
                    if temp == 1:
                        print("Hello")
                        print(start_date.month)
                        print(end_date.month)
                        profCal2 = ProfessionalSalaryCal.objects.filter(
                            empcode=emp.empcode,
                            year = s_year,
                            month_int__gte = start_date.month,
                            month_int__lte = end_date.month
                        )
                        print(profCal2)
                    elif temp == 2:
                        profCal2_1 = ProfessionalSalaryCal.objects.filter(
                            empcode = emp.empcode,
                            year=s_year,
                            month_int__gte=  start_date.month,
                            month_int__lte = 12
                        )
                        profCal2_2 = ProfessionalSalaryCal.objects.filter(
                            empcode=emp.empcode,
                            year=e_year,
                            month_int__gte=1,
                            month_int__lte=end_date.month
                        )
                        profCal2 = profCal2_1.union(profCal2_2)
                        print(profCal2)
                    p = inflect.engine()
                    app_sal = profCal.appSalary
                    prof_f = profCal.professionalFees
                    o_earn = profCal.other_earning
                    pro_in = profCal.profIncentive
                    gross_e = profCal.grossEarn
                    o_ded = profCal.other_deduction
                    inc_tax = profCal.incomeT
                    gros_ded = profCal.grossDed
                    net_s = profCal.netSal
                    if 0 <= app_sal < 10**12 :
                        app_sal = "{:,.2f}".format(app_sal)
                    if 0 <= prof_f < 10**12 :
                        prof_f = "{:,.2f}".format(prof_f)
                    if 0 <= o_earn < 10**12 :
                        o_earn = "{:,.2f}".format(o_earn)
                    if 0 <= pro_in < 10**12 :
                        pro_in = "{:,.2f}".format(pro_in)
                    if 0 <= gross_e < 10**12 :
                        gross_e = "{:,.2f}".format(gross_e)
                    if 0 <= o_ded < 10**12 :
                        o_ded = "{:,.2f}".format(o_ded)
                    if 0 <= inc_tax < 10**12 :
                        inc_tax = "{:,.2f}".format(inc_tax)
                    if 0 <= gros_ded < 10**12 :
                        gros_ded = "{:,.2f}".format(gros_ded)
                    if 0 <= net_s < 10**12 :
                        net_s = "{:,.2f}".format(net_s)
                    if 0 <= profCal.netSal < 10**12:
                        amount = p.number_to_words(profCal.netSal)
                        if amount.endswith(" point zero"):
                            amount = amount[:-len(" point zero")]
                    app_sal_all = 0.0
                    prof_f_all = 0.0
                    o_ean_all = 0.0
                    pro_in_all = 0.0
                    gross_e_all = 0.0
                    o_ded_all = 0.0
                    inc_tax_all = 0.0
                    gros_ded_all = 0.0
                    for cale in profCal2:
                        app_sal_all += cale.appSalary
                        prof_f_all += cale.professionalFees
                        o_ean_all += cale.other_earning
                        pro_in_all += cale.profIncentive
                        gross_e_all += cale.grossEarn
                        o_ded_all += cale.other_deduction
                        inc_tax_all += cale.incomeT
                        gros_ded_all += cale.grossDed
                    if 0 <= app_sal_all < 10**12 :
                        app_sal_all = "{:,.2f}".format(app_sal_all)
                    if 0 <= prof_f_all < 10**12 :
                        prof_f_all = "{:,.2f}".format(prof_f_all)
                    if 0 <= o_ean_all < 10**12 :
                        o_ean_all = "{:,.2f}".format(o_ean_all)
                    if 0 <= pro_in_all < 10**12 :
                        pro_in_all = "{:,.2f}".format(pro_in_all)
                    if 0 <= gross_e_all < 10**12 :
                        gross_e_all = "{:,.2f}".format(gross_e_all)
                    if 0 <= o_ded_all < 10**12 :
                        o_ded_all = "{:,.2f}".format(o_ded_all)
                    if 0 <= inc_tax_all < 10**12 :
                        inc_tax_all = "{:,.2f}".format(inc_tax_all)
                    if 0 <= gros_ded_all < 10**12 :
                        gros_ded_all = "{:,.2f}".format(gros_ded_all)
                    flag = "no"
            except:
                flag = "yes"


    return render(request, 'paySlip.html', locals())

def generateSlip(request):
    user = request.user
    if request.method == 'POST':
        selected_month = int(request.POST.get('month'))
        selected_year = int(request.POST.get('year'))

        # Get the calendar for the specified month and year
        cal = calendar.monthcalendar(selected_year, selected_month)

        saturdays = 0
        sundays = 0

        for week in cal:
            # Saturday is represented by index 5 and Sunday by index 6 in the week
            saturdays += 1 if week[calendar.SATURDAY] != 0 else 0
            sundays += 1 if week[calendar.SUNDAY] != 0 else 0

        # Query the attendance records for the employee for the selected month
        # Assuming the field 'is_present' indicates the employee's presence on that day
        print(saturdays, sundays)
    return render(request, 'generateSlip.html',locals())


def addEmpDetails(request):
    if not request.user.is_authenticated:
        return redirect('adminLogin')
    error = ""
    if request.method == "POST":
        ei = request.POST['emailid']
        dept = request.POST['empDep']
        des = request.POST['empDes']
        cont = request.POST['empContact']
        doj = request.POST['jdate']
        gend = request.POST['gender']
        man = request.POST['manager']
        dobb = request.POST['db']
        an = request.POST['adharno']
        pfn = request.POST['pf']
        un = request.POST['uann']
        eip = request.POST['esic']
        bn = request.POST['bname']
        acn = request.POST['acno']
        ic = request.POST['ifscno']
        etype = request.POST['employeeType']
        leaveD = request.POST['ldate']
        stat = request.POST['status']
        cname = request.POST['company']
        user = User.objects.get(username=ei)
        employee = EmployeeDetail.objects.get(user=user)
        employee.empdept = dept
        employee.designation =des
        employee.contact = cont
        employee.gender = gend
        employee.manage = man
        employee.adhar = an
        employee.pfno = pfn
        employee.uan = un
        employee.esicip = eip
        employee.bank = bn
        employee.ifsc = ic
        employee.accountno = acn
        employee.emptype = etype
        employee.status = stat
        employee.company_name = cname
        employee.joiningDate = doj
        if dobb :
            employee.dob = dobb
        if dobb == '' :
            employee.dob = None
        if leaveD:
            employee.leavingDate = leaveD
        if leaveD == '' :
            employee.leavingDate = None
        if des == "Manager":
            user.is_staff = 1
            user.save()
        try:
            employee.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'addEmpDetails.html', locals())

def editProfile(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    try :
        if request.method == "POST":
            fname = request.POST['firstname']
            lname = request.POST['lastname']
            depart = request.POST['empDep']
            desi = request.POST['empDes']
            mobile = request.POST['empContact']
            reportM = request.POST['manager']
            dateofB = request.POST['db']
            adharn = request.POST['adharno']
            proN = request.POST['pf']
            uanno = request.POST['uann']
            esicno = request.POST['esic']
            bankName = request.POST['bname']
            actno = request.POST['acno']
            ifscCode = request.POST['ifscno']
            dateofJ = request.POST['jdate']
            print(fname, lname, depart, desi, mobile, reportM, 
              dateofB, adharn, proN, uanno, esicno, bankName,
              actno, ifscCode, dateofJ)
            if fname :
                employee.user.first_name = fname
            if lname :
                employee.user.last_name = lname
            if depart:
                employee.empdept = depart
            if desi:
                employee.designation = desi
            if mobile:
                employee.contact = mobile
            if reportM:
                employee.manage = reportM
            if dateofB:
                employee.dob = dateofB
            if adharn:
                employee.adhar = adharn
            if proN:
                employee.pfno = proN
            if uanno:
                employee.uan = uanno
            if esicno:
                employee.esicip = esicno
            if bankName:
                employee.bank = bankName
            if actno:
                employee.accountno = actno
            if ifscCode:
                employee.ifsc = ifscCode
            if dateofJ:
                employee.joiningDate = dateofJ
            employee.save()
            error = "no"
    except:
        error="yes"

    return render(request, "editProfile.html", locals())

'''
#not using this function
def approveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()
    return redirect('viewLeaveApplication')

#not using this function
def disapproveLeave(request,id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()
    return redirect('viewLeaveApplication')
'''
def approveLeave2(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()

    # Mark the attendance for the approved leave
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    if leave.leave_type == 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            attendSummary.paid_leave += 1
            attendance.save()
            attendSummary.save()
        attendSummary.biMOB = attendSummary.biMOB - len(date_range)
        
        
        
    if start_date.month == end_date.month and leave.leave_type != 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            if leave.leave_type != "Optional Holiday" :
                attendSummary.paid_leave += 1
            else :
                attendSummary.unpaid_leave +=1
            attendance.save()
            attendSummary.save()
    if start_date.month != end_date.month and leave.leave_type != 'Bi-monthly Offs':
        attendSummary1, created1 = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                 days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        print(attendSummary1)
        attendSummary2, created2 = AttendanceSummary.objects.get_or_create(user=user, month=end_date.month, year=end_date.year,
                                                                days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary1.paid_leave +=1
                else:
                    attendSummary1.unpaid_leave +=1
                attendance.save()
                attendSummary1.save()
            if date.month == end_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary2.paid_leave +=1
                else:
                    attendSummary2.unpaid_leave +=1
                attendance.save()
                attendSummary2.save()

    return redirect('viewLeaveApplication')

def disapproveLeave2(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()

    # Mark the attendance for the disapproved leave as 0
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    emp = EmployeeDetail.objects.get(user=user)
    if leave.leave_type == "Earned Leave":
        emp.earnedLeaveB += len(date_range)
        emp.save()
    elif leave.leave_type == "Sick Leave":
        emp.sickLeaveB += len(date_range)
        emp.save()
    elif leave.leave_type == "Freedom From Covid Leave":
        emp.ffcB += len(date_range)
        emp.save()
    elif leave.leave_type == "Maternity Leave":
        emp.maternityLB += len(date_range)
        emp.save()
    elif leave.leave_type == "Optional Holiday (OH)":
        emp.oH2B += len(date_range)
        emp.save()
    elif leave.leave_type == "Optional Holiday":
        emp.oHB += len(date_range)
        emp.save()
    elif leave.leave_type ==  'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year)
        attendSummary.biMOB += len(date_range)
        attendSummary.save()
    
    for date in date_range:
        attendance, created = Attend.objects.get_or_create(user=user, date=date)
        attendance.is_present = 0
        attendance.save()

    return redirect('viewLeaveApplication')


def staffSalary(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = StaffSalary.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.salary_csv.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)

    return render(request,'StaffSalary.html',locals())

def update_fields(request):
    if request.method == 'POST':
        empcode = request.POST.get('0')  # Get the empcode from the hidden input
        print(empcode)
        employee_detail_instance = EmployeeDetail.objects.get(empcode=empcode)
        staff,created = StaffSalary.objects.get_or_create(empcode=employee_detail_instance)

        # Update the fields based on the form data
        staff.basic = request.POST.get('1')  # Use proper indexes for other fields
        staff.hra = request.POST.get('2')
        staff.specialAll = request.POST.get('3')
        staff.grossS = request.POST.get('4')
        staff.syear = request.POST.get('5')
        staff.save()

        return redirect('staffSalary')  # Redirect back to the salary page


def employee_salary_detail(request):
    try:
        employee_detail = EmployeeDetail.objects.get(user=request.user)
        staff_salary = StaffSalary.objects.get(empcode=employee_detail)
    except (EmployeeDetail.DoesNotExist, StaffSalary.DoesNotExist):
        employee_detail = None
        staff_salary = None


    return render(request, 'employee_salary_detail.html', locals())

def OpenIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = Incentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.inc_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
    # Process CSV data and apply calculations
    for row in csv_data:
        reds_per = int(row[4])
        inc1=0
        if reds_per <= 20 :
            inc1 = 5
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 4
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 3
        elif reds_per > 40 :
            inc1 = 2
        
        # Replace the inc1 value in the corresponding row
        row[6] = str(inc1)  # Assuming inc1 column is at index 5
        row[7] = str(f"{int(row[6])*int(row[2]):.2f}")
        #print(row[6])

        nps = int(row[8].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 2
        elif nps >50 and nps <= 60:
            inc2 = 3
        elif nps >60 and nps <= 70:
            inc2 = 4
        elif nps > 70 :
            inc2 = 5
        
        row[9] = str(inc2)
        row[10] = str(f"{int(row[9])*int(row[2]):.2f}")
        qrs = int(row[11].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 2
        elif qrs > 60 and qrs <= 70:
            inc3 = 3
        elif qrs > 70 and qrs <= 80 :
            inc3 = 4
        elif qrs > 80 :
            inc3 = 5
        
        row[12] = str(inc3)
        row[13] = str(f"{int(row[12])*int(row[2]):.2f}")
        row[14] = str(int(row[6])+ int(row[9]) + int(row[12]))
        row[15] = str(f"{float(row[7]) + float(row[10]) + float(row[13]):.2f}")
        row[17] = str(f"{int(row[16])*2*int(row[14]):.2f}")
        row[19] = str(f"{round(int(row[18])*0.25*int(row[14])):.2f}")
        #print(row[18])
        row[21] = str(f"{float(row[15])+ float(row[17]) + float((row[19])):.2f}")
        #print(row[20])
        if row[22] != '':
            row[23] = str(f"{float(row[21]) + float(row[22]):.2f}")
        else:
            row[23] = str(f"{float(row[21]):.2f}")
        row[24] = str(f"{round(float(row[23])*0.1):.2f}")
        row[25] = str(f"{float(row[23]) - float(row[24]):.2f}")



    context = {
        'csv_data': csv_data,
        'column_names': column_names,
    }

    return render(request, 'Incentive.html', context)

def OpenDoctorIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = DoctorIncentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.inc_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
    selected_month = ''
    selected_year = ''
    column_names.append('Month')
    column_names.append('Year')
    month_dict = {'':'','1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', 
                  '10':'October', '11':'November', '12':'December'}
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
    for row in csv_data:
        row.append(month_dict[selected_month])
        row.append(selected_year)
        reds_per = int(row[4].strip('%'))
        inc1=0
        if reds_per <= 20 :
            inc1 = 30
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 24
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 18
        elif reds_per > 40 :
            inc1 = 12
        
        # Replace the inc1 value in the corresponding row
        row[5] = str(inc1)  # Assuming inc1 column is at index 5
        row[6] = str(f"{int(row[5])*int(row[1]):.2f}")
        nps = int(row[7].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 12
        elif nps >50 and nps <= 60:
            inc2 = 18
        elif nps >60 and nps <= 70:
            inc2 = 24
        elif nps > 70 :
            inc2 = 30
        
        row[8] = str(inc2)
        row[9] = str(f"{int(row[8])*int(row[1]):.2f}")

        qrs = int(row[10].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 12
        elif qrs > 60 and qrs <= 70:
            inc3 = 18
        elif qrs > 70 and qrs <= 80 :
            inc3 = 24
        elif qrs > 80 :
            inc3 = 30
        
        row[11] = str(inc3)
        row[12] = str(f"{int(row[11])*int(row[1]):.2f}")
        row[13] = str(int(row[5])+ int(row[8]) + int(row[11]))
        row[14] = str(f"{float(row[6]) + float(row[9]) + float(row[12]):.2f}")
        row[16] = str(f"{round(int(row[13])*0.25*int(row[15])):.2f}")
        row[17] = str(f"{float(row[14]) + float(row[16]):.2f}")
        if row[18] != '':
            row[19] = str(f"{float(row[17]) + float(row[18]):.2f}")
        else:
            row[19] = str(f"{float(row[17]):.2f}")
        row[20] = str(f"{round(float(row[19])*0.1):.2f}")
        row[21] = str(f"{float(row[19]) - float(row[20]):.2f}")


    return render(request, 'doctorIncentive.html', locals())

def OpenDietIncentive(request):
    # Assuming you have an instance of EmployeeDetail
    employee_detail_instance = EmployeeDetail.objects.get(user=request.user)

    # Now you can query StaffSalary using the employee_detail_instance
    staff = DietIncentive.objects.get(empcode=employee_detail_instance)
    # Read the CSV file
    csv_file_path = staff.diet_file.path  # Make sure to use the correct field name
    csv_data = []
    column_names = []

    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                column_names = row  # Store column names from the first row
            else:
                csv_data.append(row)
# Update csv_data with selected_month and selected_year
    for row in csv_data:
        reds_per = int(row[5].strip('%'))
        inc1=0
        if reds_per <= 20 :
            inc1 = 10
        elif reds_per > 20 and reds_per <= 30 :
            inc1 = 8
        elif reds_per > 30 and reds_per <= 40 :
            inc1 = 6
        elif reds_per > 40 :
            inc1 = 4
        # Replace the inc1 value in the corresponding row
        row[6] = str(inc1)  # Assuming inc1 column is at index 5
        row[7] = str(f"{int(row[6])*int(row[2]):.2f}")
        nps = int(row[8].strip('%'))
        inc2=0
        if nps <= 50 :
            inc2 = 4
        elif nps >50 and nps <= 60:
            inc2 = 6
        elif nps >60 and nps <= 70:
            inc2 = 8
        elif nps > 70 :
            inc2 = 10
        
        row[9] = str(inc2)
        row[10] = str(f"{int(row[9])*int(row[2]):.2f}")

        qrs = int(row[11].strip('%'))
        inc3=0
        if qrs <= 60 :
            inc3 = 4
        elif qrs > 60 and qrs <= 70:
            inc3 = 6
        elif qrs > 70 and qrs <= 80 :
            inc3 = 8
        elif qrs > 80 :
            inc3 = 10
        
        row[12] = str(inc3)
        row[13] = str(f"{int(row[12])*int(row[2]):.2f}")
        row[14] = str(int(row[6])+ int(row[9]) + int(row[12]))
        row[15] = str(f"{float(row[7]) + float(row[10]) + float(row[13]):.2f}")
        row[17] = str(f"{round(int(row[16])*2*int(14)):.2f}")
        row[19] = str(f"{round(int(row[18])*0.25*int(row[14])):.2f}")
        row[21] = str(f"{float(row[15]) + float(row[17]) + float(row[19]):.2f}")
        row[22] = str(f"{round(float(row[21])*0.1):.2f}")
        row[23] = str(f"{float(row[21]) - float(row[22]):.2f}")


    return render(request, 'dietIncentive.html', locals())


def salaryCalculation1(request):
    selected_month1 = 'August'
    selected_year = 2023
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    selected_month = month_dict[selected_month1]
    # Retrieve StaffSalary and AttendanceSummary data for the selected month and year
    staff_data = StaffSalary.objects.select_related('empcode__user', 'empcode').filter(syear=selected_year).all()
    attendance_data = AttendanceSummary.objects.select_related('user').filter(month=selected_month, year=selected_year)

    # Create a dictionary to store attendance data by user ID
    attendance_dict = {attendance.user_id: attendance for attendance in attendance_data}

    # Combine data for the same employees
    combined_data = []
    for staff in staff_data:
        user_id = staff.empcode.user_id
        if user_id in attendance_dict:
            attendance = attendance_dict[user_id]
            combined_data.append((staff, attendance))
    return render(request, 'salaryCalculation.html',locals())


def update_doctor_fields(request):
    return redirect('update_doctor_fields')


def update_exercise_field(request):
    if request.method == 'POST':
        empcode = request.POST.get('0')  # Get the empcode from the hidden input
        print(empcode)
        employee_detail_instance = EmployeeDetail.objects.get(empcode=empcode)
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        selected_month = request.POST.get('26')
        selected_month = month_dict[selected_month]
        print(selected_month)
        selected_year = request.POST.get('27')
        staff,created = Incentive.objects.get_or_create(empcode=employee_detail_instance, imonth=selected_month, iyear=selected_year)
        staff.totAllottedPart = request.POST.get('2')
        staff.totalPartWI0 = request.POST.get('3')
        staff.totalPatientsInred = request.POST.get('4')
        staff.redsPer = request.POST.get('5')
        staff.inc1 = request.POST.get('6')
        staff.amt1 = request.POST.get('7')
        staff.nps = request.POST.get('8')
        staff.inc2 = request.POST.get('9')
        staff.amt2 = request.POST.get('10')
        staff.qrs = request.POST.get('11')
        staff.inc3 = request.POST.get('12')
        staff.amt3 = request.POST.get('13')
        staff.totalEffortInc = request.POST.get('14')
        staff.totalEffortIncPayout = request.POST.get('15')
        staff.vipParticipants = request.POST.get('16')
        staff.amtVipParticipants = request.POST.get('17')
        staff.intPartiAll = request.POST.get('18')
        staff.addPayIntParti = request.POST.get('19')
        amtIntPart1 = request.POST.get('20')
        if amtIntPart1:
            staff.amtIntPart = amtIntPart1
        else:
            staff.amtIntPart = 0.00
        staff.totalFinalPayout = request.POST.get('21')
        trp1 = request.POST.get('22')
        if trp1:
            staff.trp = trp1
        else:
            staff.trp = 0.00
        staff.addTotalFinalPayout = request.POST.get('23')
        staff.lessTDS = request.POST.get('24')
        staff.netPayout = request.POST.get('25')
        staff.save()
    return redirect('incentive')

def salaryCalculation(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    s_year = 0
    e_year = 0
    if selected_month in ['January', 'February', 'March'] :
        e_year = int(selected_year)
        s_year = int(selected_year) -1
        
    elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
        s_year = int(selected_year)
        e_year = int(selected_year) + 1
    salary = StaffSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year)
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    numMonth = month_dict[selected_month]
    # Retrieve StaffSalary and AttendanceSummary data for the selected month and year
    staff_emp = EmployeeDetail.objects.filter(emptype='Staff')
    print(staff_emp)
    staff_users = staff_emp.values_list('user', flat=True)
    attendS = AttendanceSummary.objects.filter(
        user__in = staff_users,
        month = numMonth,
        year = selected_year
    )
    employee_codes = EmployeeDetail.objects.filter(user__in=staff_users).values('user','empcode')
    employee_code_map = {entry['user']: entry['empcode'] for entry in employee_codes}
    attend_data = [
    {
        'employee_code': employee_code_map[emp.user.id],
        'employee_name': f"{emp.user.first_name} {emp.user.last_name}",
        'selected_month': selected_month,
        'selected_year': selected_year,
        'days_present': emp.days_present,
        'days_total': emp.days_total,
    }
    for emp in attendS
    ]
    context = {
        'attendSum_data' : attend_data,
    }
    return render(request, 'salaryCalculation.html',context)

def add_salary_calculation(request):
    error = ""
    if request.method == 'POST':
        empcode = request.POST.get('empcode')
        print(empcode)
        empname = request.POST.get('empN')
        print(empname)
        selected_month = request.POST.get('month')
        print(selected_month)
        selected_year = request.POST.get('year')
        print(selected_year)
        others_earning = request.POST.get('others_earn')
        print(others_earning)
        other_ded = request.POST.get('others_deduction')
        print(other_ded)
        if others_earning :
            others_earning = float(others_earning)
        else :
            others_earning = 0.0
        if other_ded :
            other_ded = float(other_ded)
        else :
            other_ded = 0.0
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        try :
            staff = StaffSalaryStructure.objects.get(empcode=empcode, start_year=s_year, end_year=e_year)
            if staff:
                error = "no"
                pass
        except:
            error = "yes"
            return HttpResponse("Salary structure of this employee for this year is not generated yet")
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        incMonth = selected_month
        selected_month = month_dict[selected_month]
        attendanceS= AttendanceSummary.objects.get(user=staff.empcode.user, month=selected_month, year=selected_year)
        total_days = attendanceS.days_present + attendanceS.paid_leave + attendanceS.sundays
        #print(total_days)
        bas_a = float(round((staff.basic * total_days)/attendanceS.days_total))
        #print(bas_a)
        hra_a_t = float(round((staff.hra * total_days)/attendanceS.days_total))
        #print(hra_a_t)
        spe_All_a = float(round((staff.specialAll * total_days)/attendanceS.days_total))
        #print(spe_All_a)
        gross_earn = bas_a + hra_a_t + spe_All_a + others_earning
        #print(gross_earn)
        pf_ded =float(round(min(staff.basic, 15000)*0.12))
        #print(pf_ded)
        esic_ded = 0.0
        if staff.grossS <= 21000:
            esic_ded = float(round(0.0075*gross_earn))
        #print(esic_ded)
        prof_tax = 0.0
        if staff.empcode.gender == 'Male':
            if selected_month == 2:
                prof_tax = float(300)
            elif gross_earn < float(7500):
                prof_tax = 0.0
            elif gross_earn >= float(7500) and gross_earn < float(10000):
                prof_tax = float(175)
            elif gross_earn >= 10000 :
                prof_tax = float(200)
        elif staff.empcode.gender == 'Female':
            if selected_month == 2:
                prof_tax = float(300)
            elif gross_earn < float(25000):
                prof_tax = 0.0
            elif gross_earn >= float(25000):
                prof_tax = float(200)
        #print(prof_tax)
        gross_ded = pf_ded + esic_ded + prof_tax + other_ded
        #print(gross_ded)
        net_sal = gross_earn - gross_ded
        #print(net_sal)
        emp = EmployeeDetail.objects.get(empcode = empcode)
        salaryCal, created = StaffSalaryCalculation.objects.get_or_create(
            empcode=emp,
            month=incMonth,
            year=selected_year,
        )
        salaryCal.paid_days = total_days + attendanceS.sundays
        salaryCal.basic_a = bas_a
        salaryCal.hra_a = hra_a_t
        salaryCal.specialAll_a = spe_All_a
        salaryCal.grossS_a = gross_earn
        salaryCal.professional_tax = prof_tax
        salaryCal.others = others_earning
        salaryCal.pf_deduction = pf_ded
        salaryCal.esic_deduction = esic_ded
        salaryCal.other_deduction = other_ded
        salaryCal.gross_deduction = gross_ded
        salaryCal.netSalary = net_sal
        salaryCal.save()
    return HttpResponseRedirect(reverse('salaryCalculation') + f'?month={incMonth}&year={selected_year}')

def DownloadStaffSalary(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        #end_m = request.POST.get('end_m')
        #end_y = request.POST.get('end_y')
        staffCal = StaffSalaryCalculation.objects.filter(month=selected_month, year=selected_year)
        print(staffCal)
        s_year = 0
        e_year = 0
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        staffStruct = StaffSalaryStructure.objects.filter(start_year=s_year, end_year=e_year)
        print(staffStruct)
        # Prepare a list of dictionaries to hold all required data
        combined_data = []

        for emp in staffCal:
            empcode = emp.empcode.empcode
            empName = emp.empName
            paid_days = emp.paid_days
            basic_a = emp.basic_a
            hra_a = emp.hra_a
            specialAll_a = emp.specialAll_a
            grossS_a = emp.grossS_a
            others = emp.others
            incentive = emp.incentive
            pf_deduction = emp.pf_deduction
            esic_deduction = emp.esic_deduction
            professional_tax = emp.professional_tax
            other_deduction = emp.other_deduction
            gross_deduction = emp.gross_deduction
            income_tax = emp.income_tax
            netSalary = emp.netSalary
            month = emp.month
            year = emp.year
            # Add other fields as needed

            # Find the matching StaffSalaryStructure record and extract data
            structure_record = staffStruct.filter(empcode=emp.empcode).first()
            if structure_record:
                basic = structure_record.basic
                hra = structure_record.hra
                specialAll = structure_record.specialAll
                grossS = structure_record.grossS
            else:
                basic = hra = specialAll = grossS = 0.0

            combined_data.append({
                'empcode': empcode,
                'empName': empName,
                'paid_days':paid_days,
                'basic_a': basic_a,
                'hra_a': hra_a,
                'specialAll_a': specialAll_a,
                'basic': basic,
                'hra': hra,
                'specialAll': specialAll,
                'grossS':grossS,
                'grossS_a':grossS_a,
                'others':others,
                'incentive':incentive,
                'pf_deduction':pf_deduction,
                'esic_deduction':esic_deduction,
                'professional_tax':professional_tax,
                'other_deduction':other_deduction,
                'gross_deduction':gross_deduction,
                'income_tax':income_tax,
                'netSalary':netSalary,
                'month':month,
                'year':year,

                # Add other fields as needed
            })
    return render(request, 'DownloadStaffSalary.html', locals())

def DownloadProfessionalSalary(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        profCal = ProfessionalSalaryCal.objects.filter(month=selected_month, year=selected_year)
        s_year = 0
        e_year = 0
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        profStruct = ProfessionalSalaryStructure.objects.filter(start_year=s_year, end_year=e_year)
        combined_data = []
        for emp in profCal:
            empcode = emp.empcode.empcode
            empName = emp.empName
            payDays = emp.payDays
            appSalary = emp.appSalary
            professionalFees = emp.professionalFees
            other_earning = emp.other_earning
            other_deduction = emp.other_deduction
            profIncentive = emp.profIncentive
            grossEarn = emp.grossEarn
            incomeT = emp.incomeT
            grossDed = emp.grossDed
            netSal = emp.netSal
            month = emp.month
            year = emp.year
            structure_record = profStruct.filter(empcode=emp.empcode).first()
            if structure_record:
                app_salary = structure_record.app_salary
                professional_fees = structure_record.professional_fees
            else:
                app_salary=professional_fees=0.0
            combined_data.append(
                {
                    'empcode':empcode,
                    'empName':empName,
                    'payDays':payDays,
                    'appSalary':appSalary,
                    'professionalFees':professionalFees,
                    'other_earning':other_earning,
                    'other_deduction':other_deduction,
                    'profIncentive':profIncentive,
                    'grossEarn':grossEarn,
                    'incomeT':incomeT,
                    'grossDed':grossDed,
                    'netSal':netSal,
                    'month':month,
                    'year':year,
                    'app_salary':app_salary,
                    'professional_fees':professional_fees,
                }
            )



    return render(request, 'DownloadProfessionalSalary.html', locals())

def viewExcerciseIncentive1(request):
    exerInc = ExcerciseInce1.objects.filter(month='August', year=2023)
    for emp in exerInc:
        reds = int(emp.calling_reds.strip('%'))
        if reds < 20 :
            emp.incentive_1 = 5
        elif reds >= 20 and reds < 30:
            emp.incentive_1 = 4
        elif reds >= 30 and reds < 40:
            emp.incentive_1 = 3
        elif reds >= 40:
            emp.incentive_1 = 2
        emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
        nps = int(emp.nps_percent.strip('%'))
        if nps < 50 :
            emp.incentive_2 = 2
        elif nps >= 50 and nps < 60 :
            emp.incentive_2 = 3
        elif nps >= 60 and nps < 70 :
            emp.incentive_2 = 4
        elif nps >= 70 :
            emp.incentive_2 = 5
        emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
        qrs = int(emp.qrs_percent.strip('%'))
        if qrs < 60 :
            emp.incentive_3 = 2
        elif qrs >= 60 and qrs < 70 :
            emp.incentive_3 = 3
        elif qrs >= 70 and qrs < 80 :
            emp.incentive_3 = 4
        elif qrs >= 70 :
            emp.incentive_3 = 5
        emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
        emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
        emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
        emp.amount_vip_participant = float(emp.total_effort_incentive * 2 * emp.vip_participants)
        emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
        emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
        emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
        emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
        emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
    return render(request, 'viewExcerciseIncentive.html',locals())

def viewExcerciseIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        exerInc = ExcerciseInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in exerInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 5
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 4
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 3
                elif reds >= 40:
                    emp.incentive_1 = 2
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 2
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 3
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 4
                elif nps >= 70 :
                    emp.incentive_2 = 5
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 2
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 3
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 4
                elif qrs >= 80 :
                    emp.incentive_3 = 5
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.amount_vip_participant = float(emp.total_effort_incentive * 2 * emp.vip_participants)
                emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
                emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
                emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
                emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
                emp.save()
            else :
                #print("Hello")
                pass
    return render(request, 'viewExcerciseIncentive.html',locals())

def viewDoctorIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        doctInc = DoctorInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in doctInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 30
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 24
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 18
                elif reds >= 40:
                    emp.incentive_1 = 12
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 12
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 18
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 24
                elif nps >= 70 :
                    emp.incentive_2 = 30
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 12
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 18
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 24
                elif qrs >= 80 :
                    emp.incentive_3 = 30
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.add_pay_for_international_participant = float(round(emp.total_effort_incentive * 0.25 * emp.international_participant_alloted))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.add_pay_for_international_participant
                emp.final_effort_incentive_payout = emp.total_effort_incentive_payout + emp.trp
                emp.less_tds = float(round(emp.final_effort_incentive_payout * 0.1))
                emp.net_payout = emp.final_effort_incentive_payout - emp.less_tds
                emp.save()
            else :
                #print("Hello")
                pass
    return render(request, 'viewDoctorIncentive.html', locals())


def viewDietIncentive(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        diInc = DietInce1.objects.filter(month=selected_month, year=selected_year)
        #print("Hello")
        #inc = exerInc[0].incentive_1
        for emp in diInc:
            inc = emp.incentive_1
            #print(inc)
            if inc == 0 :
                #print("hi")
                reds = int(emp.calling_reds.strip('%'))
                if reds < 20 :
                    emp.incentive_1 = 10
                elif reds >= 20 and reds < 30:
                    emp.incentive_1 = 8
                elif reds >= 30 and reds < 40:
                    emp.incentive_1 = 6
                elif reds >= 40:
                    emp.incentive_1 = 4
                emp.amount_1 = float(emp.incentive_1 * emp.total_no_of_allotted_participants)
                nps = int(emp.nps_percent.strip('%'))
                if nps < 50 :
                    emp.incentive_2 = 4
                elif nps >= 50 and nps < 60 :
                    emp.incentive_2 = 6
                elif nps >= 60 and nps < 70 :
                    emp.incentive_2 = 8
                elif nps >= 70 :
                    emp.incentive_2 = 10
                emp.amount_2 = float(emp.incentive_2 * emp.total_no_of_allotted_participants)
                qrs = int(emp.qrs_percent.strip('%'))
                if qrs < 60 :
                    emp.incentive_3 = 4
                elif qrs >= 60 and qrs < 70 :
                    emp.incentive_3 = 6
                elif qrs >= 70 and qrs < 80 :
                    emp.incentive_3 = 8
                elif qrs >= 80 :
                    emp.incentive_3 = 10
                emp.amount_3 = float(emp.incentive_3 * emp.total_no_of_allotted_participants)
                emp.total_effort_incentive = emp.incentive_1 + emp.incentive_2 + emp.incentive_3
                emp.total_effort_payout = float(emp.total_effort_incentive * emp.total_no_of_allotted_participants)
                emp.amount_vip_participant = float(emp.vip_patients * 2 * emp.total_effort_incentive)
                emp.add_pay_for_international_participant = float(round(emp.international_participant_alloted * 0.25 * emp.total_effort_incentive))
                emp.total_effort_incentive_payout = emp.total_effort_payout + emp.amount_vip_participant + emp.add_pay_for_international_participant
                emp.less_tds = float(round(emp.total_effort_incentive_payout * 0.1))
                emp.net_payout = emp.total_effort_incentive_payout - emp.less_tds
                emp.save()
            else:
                pass
    return render(request, 'viewDietIncentive.html', locals())


def professionalSalaryCalculation(request):
    error = 0
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
            
        
        salary_structure_exists = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year).exists()
        if salary_structure_exists :
            
            salary = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year)
            month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}           
            # First, filter employees based on empType
            professional_employees = EmployeeDetail.objects.filter(emptype='Professional')
            # Get the User objects for professional employees
            professional_users = professional_employees.values_list('user', flat=True)

            # Then, filter AttendanceSummary objects for the selected month and year, related to professional employees
            attendSum = AttendanceSummary.objects.filter(
            user__in=professional_users,
            month=month_numbers[selected_month],
            year=selected_year
            )
            # After filtering the AttendanceSummary objects, retrieve the empcode for each employee
            employee_codes = EmployeeDetail.objects.filter(user__in=professional_users).values('user', 'empcode')
            # Create a dictionary to map user IDs to empcodes
            employee_code_map = {entry['user']: entry['empcode'] for entry in employee_codes}
            # Create a list of dictionaries containing the necessary information for rendering in the template
            attendSum_data = [
            {
            'employee_name': f"{emp.user.first_name} {emp.user.last_name}",
            'employee_code': employee_code_map[emp.user.id],
            'selected_month': selected_month,
            'selected_year': selected_year,
            'days_present': emp.days_present,
            'days_total': emp.days_total,
            }
            for emp in attendSum
            ]
            context = {
            'attendSum_data': attendSum_data,
            }
            
            error = 0
        else :
            error = 1

    return render(request, 'professionalSalaryCalculation.html', locals())


def add_professional_salary_calculation(request):
    error = ""
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        empC = request.POST.get('empcode')
        emp_na = request.POST.get('empN')
        otherE = request.POST.get('others')
        otherD = request.POST.get('others_deduction')
        print(empC)
        print(selected_month)
        print(selected_year)
        print(otherE)
        print(otherD)
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
        try :
            salStruct = ProfessionalSalaryStructure.objects.get(empcode=empC, start_year=s_year, end_year=e_year)
            if salStruct:
                error = "no"
                pass
        except:
            error = "yes"
            return HttpResponse("Salary structure of this employee for this year is not generated yet")
        month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7,
                      'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
        incMonth = selected_month
        selected_month = month_dict[selected_month]
        attendS = AttendanceSummary.objects.get(user=salStruct.empcode.user, month=selected_month, year=selected_year)
        presentDays = attendS.days_present + attendS.paid_leave + attendS.sundays
        app_sal_a = float(round((salStruct.app_salary * presentDays)/attendS.days_total))
        proff_fees_a = float(round((salStruct.professional_fees * presentDays)/attendS.days_total))
        if otherE :
            otherE = float(otherE)
        else:
            otherE = 0.0
        if otherD :
            otherD = float(otherD)
        else :
            otherD = 0.0
        inc = 0.0
        emp = EmployeeDetail.objects.get(empcode=empC)
        if salStruct.empcode.empdept == "Medical Science":
            try :
                incData = DoctorInce1.objects.get(empcode=empC, month=incMonth, year=selected_year)
                if incData:
                    inc = incData.final_effort_incentive_payout
            except :
                inc = 0.0
        if salStruct.empcode.empdept == "Exercise Science":
            try :
                incData = ExcerciseInce1.objects.get(empcode=empC, month=incMonth, year=selected_year)
                if  incData :
                    inc = incData.final_effort_incentive_payout
            except :
                inc = 0.0
        if salStruct.empcode.empdept == "Diet Science":
            try :
                incData = DietInce1.objects.get(empcode=empC, month=selected_month, year=selected_year)
                if  incData :
                    inc = incData.total_effort_incentive_payout
            except :
                inc = 0.0
        gross_earning = app_sal_a + proff_fees_a + otherE + inc
        income_tax = float(round(gross_earning * 0.1))
        gross_deduction = income_tax + otherD
        netS = gross_earning - gross_deduction
        emp = EmployeeDetail.objects.get(empcode=empC)
        profSalCal, created = ProfessionalSalaryCal.objects.get_or_create(
            empcode = emp,  month = incMonth, year = selected_year
        )
        profSalCal.empName = emp_na
        profSalCal.payDays = presentDays
        profSalCal.appSalary = app_sal_a
        profSalCal.professionalFees = proff_fees_a
        profSalCal.other_earning = otherE
        profSalCal.other_deduction = otherD
        profSalCal.profIncentive = inc
        profSalCal.grossEarn = gross_earning
        profSalCal.incomeT = income_tax
        profSalCal.grossDed = gross_deduction
        profSalCal.netSal = netS
        profSalCal.save()


    #return redirect('professionalSalaryCalculation')
    # Redirect to professionalSalaryCalculation with selected month and year as URL parameters
    return HttpResponseRedirect(reverse('professionalSalaryCalculation') + f'?month={incMonth}&year={selected_year}')


def getMonthnYear(request):
    error = 0
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
            
        
        salary_structure_exists = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year).exists()
        if salary_structure_exists :
            error = 0
        else:
            error = 1
            return HttpResponse("Professional Salary Structure for this year is not generated yet")
        # Redirect to professionalSalaryCalculation with selected month and year as URL parameters
        return redirect(reverse('professionalSalaryCalculation') + f'?month={selected_month}&year={selected_year}')
    return render(request,'getMonthnYear.html',locals())

def getMonthAndYear(request):
    error = 0
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        s_year = 0
        e_year = 0
        # Check if there is a salary structure for the selected period
        # Construct the conditions for checking if the selected month and year are within the range
        if selected_month in ['January', 'February', 'March'] :
            e_year = int(selected_year)
            s_year = int(selected_year) -1
        
        elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
            s_year = int(selected_year)
            e_year = int(selected_year) + 1
            
        
        salary_structure_exists = StaffSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year).exists()
        print(salary_structure_exists)
        if salary_structure_exists :
            error = 0
        else:
            error = 1
            return HttpResponse("Staff Salary Structure for this year is not generated yet")
        # Redirect to professionalSalaryCalculation with selected month and year as URL parameters
        return redirect(reverse('salaryCalculation') + f'?month={selected_month}&year={selected_year}')
    return render(request,'getMonthAndYear.html',locals())

'''
def professionalSalaryCalculation(request):
    selected_month = request.GET.get('month')
    selected_year = request.GET.get('year')
    s_year = 0
    e_year = 0
    print(selected_month)
    print(selected_year)
    # Check if there is a salary structure for the selected period
    # Construct the conditions for checking if the selected month and year are within the range
    if selected_month in ['January', 'February', 'March'] :
        e_year = int(selected_year)
        s_year = int(selected_year) -1
        
    elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
        s_year = int(selected_year)
        e_year = int(selected_year) + 1
    salary = ProfessionalSalaryStructure.objects.filter(start_month ="April", end_month = "March" ,start_year = s_year, end_year = e_year)
    month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}           
    # First, filter employees based on empType        
    professional_employees = EmployeeDetail.objects.filter(emptype='Professional')
    # Get the User objects for professional employees
    professional_users = professional_employees.values_list('user', flat=True)

    # Then, filter AttendanceSummary objects for the selected month and year, related to professional employees
    attendSum = AttendanceSummary.objects.filter(
    user__in=professional_users,
    month=month_numbers[selected_month],
    year=selected_year
    )
    # After filtering the AttendanceSummary objects, retrieve the empcode for each employee
    employee_codes = EmployeeDetail.objects.filter(user__in=professional_users).values('user', 'empcode')
    # Create a dictionary to map user IDs to empcodes
    employee_code_map = {entry['user']: entry['empcode'] for entry in employee_codes}
    # Create a list of dictionaries containing the necessary information for rendering in the template
    attendSum_data = [
    {
            'employee_name': f"{emp.user.first_name} {emp.user.last_name}",
            'employee_code': employee_code_map[emp.user.id],
            'selected_month': selected_month,
            'selected_year': selected_year,
            'days_present': emp.days_present,
            'days_total': emp.days_total,
    }
    for emp in attendSum
    ]
    context = {
            'attendSum_data': attendSum_data,
            }
    
    return render(request, 'professionalSalaryCalculation.html',context)
'''
def applyForLeave(request):
    if not request.user.is_authenticated:
        return redirect('empLogin')
    
    error = ""
    u = request.user
    emp = EmployeeDetail.objects.get(user=u)
    dat = datetime.now().today()
    #print(yearLeaveObj)
    attendSummary, created = AttendanceSummary.objects.get_or_create(user=u, month = dat.month, year = dat.year,
                                                                        days_total = calendar.monthrange(dat.year, dat.month)[1])
    today_month = dat.month
    today_year = dat.year
    #print(today_month)
    #print(today_year)
    yearLeaveObj3, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year, end_year = today_year)

    if request.method == "POST":
        lT = request.POST['leaveType']
        sD = request.POST['startDate']
        eD = request.POST['endDate']
        r = request.POST['reason']
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.strptime(sD, '%Y-%m-%d')
        end_date = datetime.strptime(eD, '%Y-%m-%d')
        # Get all the dates between start_date and end_date, excluding Sundays
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
        today_month1 = start_date.month
        today_year1 = start_date.year
        #print(today_month1)
        #print(today_year1)
        
        today_month2 = end_date.month
        today_year2 = end_date.year
        #print(today_month2)
        #print(today_year2)
        
        if today_year1 == today_year2 and lT == 'Sick Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            balanceD = yearLeaveObj.sickLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.sickLeaveB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif today_year1 != today_year2 and lT == 'Sick Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
            balanceD1 = yearLeaveObj1.sickLeaveB
            balanceD2 = yearLeaveObj2.sickLeaveB
            #print(balanceD1)
            #print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    #print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.sickLeaveB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.sickLeaveB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif today_year1 == today_year2 and lT == 'Earned Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            balanceD = yearLeaveObj.earnedLeaveB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.earnedLeaveB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif today_year1 != today_year2 and lT == 'Earned Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
            balanceD1 = yearLeaveObj1.earnedLeaveB
            balanceD2 = yearLeaveObj2.earnedLeaveB
            #print(balanceD1)
            #print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.earnedLeaveB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.earnedLeaveB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif today_year1 == today_year2 and lT == 'Freedom From Covid Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            balanceD = yearLeaveObj.ffcB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.ffcB = balanceD
                yearLeaveObj.save()
                error = "no"
        # if case is like 30-March-2024 to 4-April-2024
        elif today_year1 != today_year2 and lT == 'Freedom From Covid Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
            balanceD1 = yearLeaveObj1.ffcB
            balanceD2 = yearLeaveObj2.ffcB
            #print(balanceD1)
            #print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.ffcB -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.ffcB -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif today_year1 == today_year2 and lT == 'Maternity Leave':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
            balanceD = yearLeaveObj.maternityLB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.maternityLB = balanceD
                yearLeaveObj.save()
                error = "no"
        elif today_year1 != today_year2 and lT == 'Maternity Leave':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
            balanceD1 = yearLeaveObj1.maternityLB
            balanceD2 = yearLeaveObj2.maternityLB
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
                months_between = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
                #print("Months between : ",months_between)
                unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
                unique_months = list(unique_months)
                #print(unique_months)
                first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
                last_month_days = end_date.day
                #print(first_month_days)
                #print(last_month_days)
                sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
                subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
                #print(subset)
                subset[0][2]  = first_month_days
                list_len = len(subset)
                subset[list_len-1][2] = last_month_days
                #print(subset[0][2])
                #print(subset[list_len-1][2])
                #print(subset)
                #print("Sorted unique months:")
                days1 = 0 # for prev year
                days2 = 0 # for new year
                for i in range(len(subset)):
                    if subset[i][0] == today_year1:
                        days1 += subset[i][2]
                    elif subset[i][0] == today_year2:
                        days2 += subset[i][2]
                yearLeaveObj1.maternityLB -= days1
                yearLeaveObj2.maternityLB -= days2
                yearLeaveObj1.save()
                yearLeaveObj2.save()
                #print(yearLeaveObj2.maternityLB)
                error = "no"
                
            
        elif today_year1 == today_year2 and lT == 'Optional Holiday (OH)':
            yearLeaveObj, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            balanceD = yearLeaveObj.oH2B
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                yearLeaveObj.oH2B = balanceD
                yearLeaveObj.save()
                error = "no"
                
        # if case is like 30-March-2024 to 4-April-2024
        elif today_year1 != today_year2 and lT == 'Optional Holiday (OH)':
            yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
            yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
            balanceD1 = yearLeaveObj1.oH2B
            balanceD2 = yearLeaveObj2.oH2B
            #print(balanceD1)
            #print(balanceD2)
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    #print(date)
                    if date.month == start_date.month :
                        yearLeaveObj1.oH2B -= 1
                        yearLeaveObj1.save()
                    elif date.month == end_date.month :
                        yearLeaveObj2.oH2B -= 1
                        yearLeaveObj2.save()
                error = "no"
        elif start_date.month == end_date.month and lT == 'Bi-monthly Offs':
            attendSum, created = AttendanceSummary.objects.get_or_create(user=u, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
            balanceD = attendSum.biMOB
            if len(date_range) > balanceD:
                error = "yes"
            if len(date_range) <= balanceD:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                balanceD -= len(date_range)
                attendSum.biMOB = balanceD
                attendSum.save()
                error = "no"
        
        elif start_date.month != end_date.month and lT == 'Bi-monthly Offs':
            attendSum1, created1 = AttendanceSummary.objects.get_or_create(user=u, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
            attendSum2, created2 = AttendanceSummary.objects.get_or_create(user=u, month = end_date.month, year = end_date.year,
                                                                        days_total = calendar.monthrange(end_date.year, end_date.month)[1])
            balanceD1 = attendSum1.biMOB
            balanceD2 = attendSum2.biMOB
            if len(date_range) > balanceD1 + balanceD2:
                error = "yes"
            if len(date_range) <= balanceD1 + balanceD2:
                employee = ApplyForLeave.objects.create(user=u, leave_type=lT, start_date=sD, end_date=eD,
                                                    reason=r, email=emp.user.username, phone_number=emp.contact, man=emp.manage)
                for date in date_range:
                    #print(date)
                    if date.month == start_date.month:
                        attendSum1.biMOB -= 1
                        attendSum1.save()
                    elif date.month == end_date.month:
                        attendSum2.biMOB -= 1
                        attendSum2.save()
                error = "no"

    return render(request, 'applyForLeave.html', locals())


def approveLeave3(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 1
    leave.save()

    # Mark the attendance for the approved leave
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    # Get all the dates between start_date and end_date, excluding Sundays
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
    if leave.leave_type == 'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            attendSummary.paid_leave += 1
            attendance.save()
            attendSummary.save()
        attendSummary.biMOB = attendSummary.biMOB - len(date_range)
        
        
        
    if start_date.month == end_date.month and leave.leave_type != 'Bi-monthly Offs' and leave.leave_type != 'Maternity Leave':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        for date in date_range:
            attendance, created = Attend.objects.get_or_create(user=user, date=date)
            attendance.is_present = 2
            if leave.leave_type != "Optional Holiday" :
                attendSummary.paid_leave += 1
            else :
                attendSummary.unpaid_leave +=1
            attendance.save()
            attendSummary.save()
    if start_date.month != end_date.month and leave.leave_type != 'Bi-monthly Offs' and leave.leave_type != 'Maternity Leave':
        attendSummary1, created1 = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                 days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        print(attendSummary1)
        attendSummary2, created2 = AttendanceSummary.objects.get_or_create(user=user, month=end_date.month, year=end_date.year,
                                                                days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary1.paid_leave +=1
                else:
                    attendSummary1.unpaid_leave +=1
                attendance.save()
                attendSummary1.save()
            if date.month == end_date.month:
                attendance, created = Attend.objects.get_or_create(user=user, date=date)
                attendance.is_present = 2
                if leave.leave_type != "Optinal Holiday":
                    attendSummary2.paid_leave +=1
                else:
                    attendSummary2.unpaid_leave +=1
                attendance.save()
                attendSummary2.save()
    if leave.leave_type == 'Maternity Leave':
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        months_between = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
        print("Months between : ",months_between)
        unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
        unique_months = list(unique_months)
        first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
        last_month_days = end_date.day
        print(first_month_days)
        print(last_month_days)
        sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
        subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
        print(subset)
        subset[0][2]  = first_month_days
        list_len = len(subset)
        subset[list_len-1][2] = last_month_days
        print(subset[0][2])
        print(subset[list_len-1][2])
        print(subset)
        print("Sorted unique months:")
        for year, month, last_day in subset:
            print(year, calendar.month_name[month], last_day)
        
        for i in range(len(subset)):
            attendSum, created = AttendanceSummary.objects.get_or_create(user=user, month=subset[i][1], year=subset[i][0],
                                                                 days_total = subset[i][2])
            attendSum.paid_leave += subset[i][2]
            attendSum.save()
    return redirect('viewLeaveApplication')

def disapproveLeave3(request, id):
    leave = ApplyForLeave.objects.get(id=id)
    leave.is_approved = 2
    leave.save()

    # Mark the attendance for the disapproved leave as 0
    start_date = leave.start_date
    end_date = leave.end_date
    user = leave.user
    today_month1 = start_date.month
    today_year1 = start_date.year
        
    today_month2 = end_date.month
    today_year2 = end_date.year

    # Get all the dates between start_date and end_date, excluding Sundays
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1) if (start_date + timedelta(days=x)).weekday() != 6]
    print(date_range)
    emp = EmployeeDetail.objects.get(user=user)
    if today_year1 == today_year2 and leave.leave_type == "Earned Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearlyLeave.earnedLeaveB += len(date_range)
        yearlyLeave.save()
    elif today_year1 != today_year2 and leave.leave_type == 'Earned Leave':
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month =12 ,start_year = today_year1, end_year = today_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month =12 ,start_year = today_year2, end_year = today_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.earnedLeaveB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.earnedLeaveB += 1
                yearLeaveObj2.save()
    elif today_year1 != today_year2 and leave.leave_type == "Sick Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearlyLeave.sickLeaveB += len(date_range)
        yearlyLeave.save()
    elif today_year1 != today_year2 and leave.leave_type == "Sick Leave":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.sickLeaveB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.sickLeaveB += 1
                yearLeaveObj2.save()
    elif today_year1 != today_year2 and leave.leave_type == "Freedom From Covid Leave":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearlyLeave.ffcB += len(date_range)
        yearlyLeave.save()
    elif today_year1 != today_year2 and leave.leave_type == "Freedom From Covid Leave":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.ffcB += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.ffcB += 1
                yearLeaveObj2.save()
    if today_year1 == today_year2 and leave.leave_type == "Maternity Leave":
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearlyLeave.maternityLB += len(date_range)
        yearlyLeave.save()
    if today_year1 != today_year2 and leave.leave_type == "Maternity Leave":
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month = 1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month = 1, end_month = 12 ,start_year = today_year2, end_year = today_year2)
        unique_months = set((date.year, date.month, calendar.monthrange(date.year, date.month)[1]) for date in date_range)
        unique_months = list(unique_months)
        first_month_days = calendar.monthrange(start_date.year, start_date.month)[1] - start_date.day + 1
        last_month_days = end_date.day
        print(first_month_days)
        print(last_month_days)
        sorted_unique_months = sorted(unique_months, key=lambda date: (date[0], date[1]))
        subset = [[year, month, last_day] for year, month, last_day in sorted_unique_months]
        print(subset)
        subset[0][2]  = first_month_days
        list_len = len(subset)
        subset[list_len-1][2] = last_month_days
        print(subset[0][2])
        print(subset[list_len-1][2])
        print(subset)
        days1 = 0 # for prev year
        days2 = 0 # for new year
        for i in range(len(subset)):
            if subset[i][0] == today_year1:
                days1 += subset[i][2]
            elif subset[i][0] == today_year2:
                days2 += subset[i][2]
        print(days1)
        print(days2)
        yearLeaveObj1.maternityLB += days1
        yearLeaveObj2.maternityLB += days2
        yearLeaveObj1.save()
        yearLeaveObj2.save()
        
    elif today_year1 == today_year2 and leave.leave_type == "Optional Holiday (OH)":
        yearlyLeave = YearlyLeaves.objects.get(empcode=emp.empcode, start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearlyLeave.oH2B += len(date_range)
        yearlyLeave.save()
    elif today_year1 != today_year2 and leave.leave_type == "Optional Holiday (OH)":
        yearLeaveObj1, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year1, end_year = today_year1)
        yearLeaveObj2, created = YearlyLeaves.objects.get_or_create(empcode=emp,start_month =1, end_month = 12 ,start_year = today_year2, end_year = today_year1)
        for date in date_range:
            if date.month == start_date.month :
                yearLeaveObj1.oH2B += 1
                yearLeaveObj1.save()
            elif date.month == end_date.month :
                yearLeaveObj2.oH2B += 1
                yearLeaveObj2.save()
    elif start_date.month == end_date.month and leave.leave_type ==  'Bi-monthly Offs':
        attendSummary, created = AttendanceSummary.objects.get_or_create(user=user, month=start_date.month, year=start_date.year,
                                                                         days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        attendSummary.biMOB += len(date_range)
        attendSummary.save()
    elif start_date.month != end_date.month and leave.leave_type ==  'Bi-monthly Offs':
        attendSum1, created1 = AttendanceSummary.objects.get_or_create(user=user, month = start_date.month, year = start_date.year,
                                                                        days_total = calendar.monthrange(start_date.year, start_date.month)[1])
        attendSum2, created2 = AttendanceSummary.objects.get_or_create(user=user, month = end_date.month, year = end_date.year,
                                                                        days_total = calendar.monthrange(end_date.year, end_date.month)[1])
        for date in date_range:
            if date.month == start_date.month:
                attendSum1.biMOB += 1
                attendSum1.save()
            if date.month  == end_date.month:
                attendSum1.biMOB += 1
                attendSum2.save()
    for date in date_range:
        attendance, created = Attend.objects.get_or_create(user=user, date=date)
        attendance.is_present = 0
        attendance.save()

    return redirect('viewLeaveApplication')


def profSalCalculation(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        profCal = ProfessionalSalaryCal.objects.filter(month=selected_month, year=selected_year)
        print(profCal)
        month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}           
        for emp in profCal:
            netSalary = emp.netSal
            if netSalary == 0.0 :
                s_year = 0
                e_year = 0
                if selected_month in ['January', 'February', 'March'] :
                    e_year = int(selected_year)
                    s_year = int(selected_year) -1
        
                elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
                    s_year = int(selected_year)
                    e_year = int(selected_year) + 1
                try :
                    salStruct = ProfessionalSalaryStructure.objects.get(empcode=emp.empcode, start_year = s_year, end_year=e_year)
                    print(salStruct)
                    if salStruct :
                        pass
                except :
                    return HttpResponse("Salary structure of this employee for this year is not generated yet")
                user = emp.empcode.user
                attendSum = AttendanceSummary.objects.get(user=user, month = month_numbers[selected_month], year=selected_year)
                incMonth = selected_month
                selected_month = month_numbers[selected_month]
                presentDays = attendSum.days_total - emp.lop
                app_sal_a = float(round((salStruct.app_salary * presentDays)/attendSum.days_total))
                proff_fees_a = float(round((salStruct.professional_fees * presentDays)/attendSum.days_total))
                inc = 0.0
                if salStruct.empcode.empdept == "Medical Science":
                    try :
                        incData = DoctorInce1.objects.get(empcode=emp.empcode, month= incMonth, year = selected_year)
                        if incData :
                            inc = incData.final_effort_incentive_payout
                    except :
                        inc = 0.0
                if salStruct.empcode.empdept == "Exercise Science":
                    try :
                        incData = ExcerciseInce1.objects.get(empcode=emp.empcode, month= incMonth, year=selected_year)
                        if incData :
                            inc = incData.final_effort_incentive_payout
                    except :
                        inc = 0.0
                if salStruct.empcode.empdept == "Diet Science":
                    try :
                        incData = DietInce1.objects.get(empcode=emp.empcode, month=incMonth, year=selected_year)
                        if incData:
                            inc = incData.total_effort_incentive_payout
                    except :
                        inc = 0.0
                gross_earning = app_sal_a + proff_fees_a + emp.other_earning + inc
                income_tax = float(round(gross_earning * 0.1))
                gross_deduction = income_tax + emp.other_deduction
                netS = gross_earning - gross_deduction
                emp.payDays = presentDays
                emp.appSalary = app_sal_a
                emp.professionalFees = proff_fees_a
                emp.profIncentive = inc
                emp.grossEarn = gross_earning
                emp.incomeT = income_tax
                emp.grossDed = gross_deduction
                emp.netSal = netS
                emp.save()
            
            else :
                pass


    return render(request, 'profSalaryCalculation.html', locals())

def staffSalaryCalculation(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')
        staffCal = StaffSalaryCalculation.objects.filter(month=selected_month, year=selected_year)
        print(staffCal)
        month_numbers = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}     
        for emp in staffCal :
            netSal = emp.netSalary
            if netSal == 0.0:
                #print("Hi")
                s_year = 0
                e_year = 0
                if selected_month in ['January', 'February', 'March'] :
                    e_year = int(selected_year)
                    s_year = int(selected_year) -1
        
                elif selected_month in ['April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'] :
                    s_year = int(selected_year)
                    e_year = int(selected_year) + 1
                try :
                    salStruct = StaffSalaryStructure.objects.get(empcode=emp.empcode, start_year = s_year, end_year=e_year)
                    print(salStruct)
                    if salStruct :
                        pass
                except :
                    return HttpResponse("Salary structure of this employee for this year is not generated yet")
                user = emp.empcode.user
                attendanceS, created = AttendanceSummary.objects.get_or_create(user=user, month = month_numbers[selected_month], year = selected_year, days_total = calendar.monthrange(int(selected_year), month_numbers[selected_month])[1])
                incMonth = selected_month
                selected_month = month_numbers[selected_month]
                total_days = attendanceS.days_total - emp.lop
                bas_a = float(round((salStruct.basic * total_days)/attendanceS.days_total))
                hra_a_t = float(round((salStruct.hra * total_days)/attendanceS.days_total))
                spe_All_a = float(round((salStruct.specialAll * total_days)/attendanceS.days_total))
                gross_earn = bas_a + hra_a_t + spe_All_a + emp.incentive + emp.others
                #print(gross_earn)
                pf_ded =float(round(min(salStruct.basic, 15000)*0.12))
                #print(pf_ded)
                esic_ded = 0.0
                if emp.grossS_a <= 21000:
                    esic_ded = float(round(0.0075*gross_earn))
                prof_tax = 0.0
                if emp.empcode.gender == 'Male':
                    if selected_month == 2:
                        prof_tax = float(300)
                    elif gross_earn < float(7500):
                        prof_tax = 0.0
                    elif gross_earn >= float(7500) and gross_earn < float(10000):
                        prof_tax = float(175)
                    elif gross_earn >= 10000 :
                        prof_tax = float(200)
                elif emp.empcode.gender == 'Female':
                    if selected_month == 2:
                        prof_tax = float(300)
                    elif gross_earn < float(25000):
                        prof_tax = 0.0
                    elif gross_earn >= float(25000):
                        prof_tax = float(200)
                gross_ded = pf_ded + esic_ded + prof_tax + emp.other_deduction
                net_sal = gross_earn - gross_ded
                emp.paid_days = total_days
                emp.basic_a = bas_a
                emp.hra_a = hra_a_t
                emp.specialAll_a = spe_All_a
                emp.grossS_a = gross_earn
                emp.pf_deduction = pf_ded
                emp.esic_deduction = esic_ded
                emp.professional_tax = prof_tax
                emp.gross_deduction = gross_ded
                emp.netSalary = net_sal
                emp.save()
            else :
                #print("Hello")
                pass
    return render(request, 'staffSalaryCalculation.html', locals())

def forgotPassword(request):
    try:
        if request.method == "POST":
            username = request.POST.get('emailid')
            #print(username)

            if not User.objects.filter(username=username).first():
                messages.success(request, "No user found with this username!!!")
                return redirect('forgotPassword')
            user_obj = User.objects.get(username=username)
            #print(user_obj)
            token = str(uuid.uuid4())
            prof, created = Profile.objects.get_or_create(user=user_obj)
            print(token)
            prof.forget_password_token = token
            prof.save()
            send_forget_password_mail(user_obj, token)
            messages.success(request, 'An email is sent.')

    except Exception as e:
        print(e)
    return render(request, "forgotPassword.html", locals())

def changePassword(request, token):
    print(token)
    context = {}
    try:
        Profile_obj = Profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : Profile_obj.user.id}
        if request.method == 'POST':
            new_pwd = request.POST.get('newpwd')
            confirmnew_pwd = request.POST.get('cnewpwd')
            user_id = request.POST.get('user_id')
            if user_id is None :
                messages.success(request, "No user id found!!!")
                return redirect('changePassword/{token}/')
            if new_pwd != confirmnew_pwd :
                messages.success(request,"New password and confirm new password not matching !!!")
                return redirect('changePassword/{token}/')
            user = User.objects.get(id=user_id)
            user.set_password(new_pwd)
            user.save()
            return redirect('empLogin')
    except Exception as e :
        print(e)
    return render(request, "changePassword.html", context)