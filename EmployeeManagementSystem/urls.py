"""
URL configuration for EmployeeManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employee import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage, name="HomePage"),
    path('register/', views.register, name="register"),
    path('empLogin/', views.employeeLogin, name="empLogin"),
    path('viewProfile/', views.viewProfile, name="viewProfile"),
    path('logout', views.Logout, name="logout"),
    path('adminLogin/', views.adminLogin, name="adminLogin"),
    path('empChangePassword/', views.empChangePassword, name="empChangePassword"),
    path('adminLogin/', views.adminLogin, name="adminLogin"),
    path('adminHome/', views.adminHome, name="adminHome"),
    path('adminChangePassword/', views.adminChangePassword, name="adminChangePassword"),
    path('allEmployeeDetails/', views.allEmployeeDetails, name="allEmployeeDetails"),
    path('attendanceReport/', views.attendanceReport, name="attendanceReport"),
    path('viewAttendance/', views.viewEmployeeAttendance, name="viewAttendance"),
    path('applyForLeave/', views.applyForLeave, name='applyForLeave'),
    path('viewLeaveApplication/',views.viewLeaveApplication,name="viewLeaveApplication"),
    path('approveLeave2/<str:id>',views.approveLeave3,name="approveLeave2"),
    path('disapproveLeave2/<str:id>',views.disapproveLeave3,name="disapproveLeave2"),
    path('viewEmpLeaveApplication/',views.viewEmpLeaveApplication, name="viewEmpLeaveApplication"),
    path('markAttend/',views.markAttend, name="markAttend"),
    path('markA/',views.markA,name="markA"),
    path('viewEmpAttendance/',views.viewAttendance, name = "viewEmpAttendance"),
    path('viewAttendanceReport/', views.viewAttendanceReport, name="viewAttendanceReport"),
    path('paySlip/', views.paySlip, name="paySlip"),
    path('generateSlip/', views.generateSlip, name="generateSlip"),
    path('addEmpDetails/', views.addEmpDetails, name="addEmpDetails"),
    path('attendanceSummary/', views.updateAttendanceSummary, name="attendanceSummary"),
    path('staffSalary/',views.staffSalary, name="staffSalary"),
    path('update_fields/', views.update_fields, name='update_fields'),
    path('employee_salary_detail/',views.employee_salary_detail, name="employee_salary_detail"),
    path('incentive/', views.OpenIncentive, name="incentive"),
    path('doctorIncentive/',views.OpenDoctorIncentive, name="doctorIncentive"),
    path('dietIncentive/',views.OpenDietIncentive, name="dietIncentive"),
    path('salaryCalculation/', views.staffSalaryCalculation, name='salaryCalculation'),
    path('update_doctor_fields', views.update_doctor_fields, name="update_doctor_fields"),
    path('update_exercise_field/', views.update_exercise_field, name="update_exercise_field"),
    path('add_salary_calculation/', views.add_salary_calculation, name="add_salary_calculation"),
    path('viewExcerciseIncentive/', views.viewExcerciseIncentive, name="viewExcerciseIncentive"),
    path('viewDoctorIncentive/', views.viewDoctorIncentive, name="viewDoctorIncentive"),
    path('viewDietIncentive/', views.viewDietIncentive, name="viewDietIncentive"),
    path('professionalSalaryCalculation/', views.profSalCalculation, name="professionalSalaryCalculation"),
    path('add_professional_salary_calculation/', views.add_professional_salary_calculation, name="add_professional_salary_calculation"),
    path('getMonthYear/', views.getMonthnYear, name="getMonthnYear"),
    path('getMonthAndYear/', views.getMonthAndYear, name="getMonthAndYear"),
    path('DownloadProfessionalSalary/', views.DownloadProfessionalSalary, name="DownloadProfessionalSalary"),
    path('DownloadStaffSalary/', views.DownloadStaffSalary, name="DownloadStaffSalary"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('changePassword/<token>/', views.changePassword, name="changePassword"),
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)