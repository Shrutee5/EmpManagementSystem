from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class EmployeeDetail(models.Model):
    empcode = models.CharField(primary_key=True,max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empdept = models.CharField(max_length=50, null=True)
    designation = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=50, null=True)
    joiningDate = models.DateField(null=True)
    manage = models.CharField(max_length=50, null=True)
    dob = models.DateField(null=True, blank=True)
    adhar = models.CharField(max_length=20,null=True,blank=True)
    pfno = models.CharField(max_length=20, default="Not Applicable")
    uan = models.CharField(max_length=20, default="Not Applicable")
    esicip = models.CharField(max_length=20, default="Not Applicable")
    bank = models.CharField(max_length=200, null=True,blank=True)
    ifsc = models.CharField(max_length=50, null=True,blank=True)
    accountno = models.CharField(max_length=50, null=True,blank=True)
    emptype = models.CharField(max_length=50, null=True)
    leavingDate = models.DateField(null=True, blank=True)
    status = models.CharField(default="Active",max_length=20)
    company_name = models.CharField(default="None", max_length=200)
    class Meta :
        db_table = 'EmployeeDetail'
    
    
    def __str__(self):
        return str(self.empcode)


class Attendance(models.Model):
    employee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.employee.username) + " " +str(self.date)
    

class Attend(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateField(null=True)
    is_present = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username + " " + str(self.date)


class AttendanceSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    days_present = models.PositiveIntegerField(default=0)
    days_total = models.PositiveIntegerField(default=0)
    paid_leave = models.PositiveIntegerField(default=0)
    unpaid_leave = models.PositiveIntegerField(default=0)
    biMOT = models.PositiveIntegerField(default=2)
    biMOB = models.PositiveIntegerField(default=2)
    sundays = models.PositiveIntegerField(default=0)

    def __str__(self):
        return  str(self.user.username) + " "+ str(self.month) + " " + str(self.year) + " " + str(self.days_present) + " " + str(self.days_total)

class ApplyForLeave(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    leave_type = models.CharField(max_length=50,null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.TextField(max_length=200,null=True)
    email = models.EmailField(null=True)
    man = models.EmailField(max_length=50, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    is_approved = models.IntegerField(default=0)


    
    def __str__(self):
        return "Leave Application by " + str(self.email)
    


class StaffSalary(models.Model):
    empcode = models.OneToOneField(EmployeeDetail, on_delete=models.CASCADE)
    basic = models.FloatField(default=0.00)
    hra = models.FloatField(default=0.00)
    specialAll = models.FloatField(default=0.00)
    grossS = models.FloatField(default=0.00)
    syear = models.PositiveIntegerField(default=0)
    salary_csv = models.FileField(upload_to='csv_files/', default=None, null=True)

    def __str__(self):
        return str(self.empcode)

class Incentive(models.Model):
    empcode = models.OneToOneField(EmployeeDetail, on_delete=models.CASCADE, primary_key=True) #col1
    totAllottedPart = models.PositiveIntegerField(default=0) # col2
    totalPartWI0 = models.PositiveIntegerField(default=0) # col3
    totalPatientsInred = models.PositiveIntegerField(default=0) # col4
    redsPer = models.TextField(default='0%') # col5
    inc1 = models.PositiveIntegerField(default=0) # col6
    amt1 = models.FloatField(default=0.00) # col7
    nps = models.TextField(default='0%') # col8
    inc2 = models.PositiveIntegerField(default=0) # col9
    amt2 = models.FloatField(default=0.00) # col10
    qrs = models.TextField(default='0%') # col11
    inc3 = models.PositiveIntegerField(default=0) # col12
    amt3 = models.FloatField(default=0.00) # col13
    totalEffortInc = models.PositiveIntegerField(default=0) # col14
    totalEffortIncPayout = models.FloatField(default=0.00) # col15
    vipParticipants = models.PositiveIntegerField(default=0) # col16
    amtVipParticipants = models.FloatField(default=0.00) # col17
    intPartiAll = models.PositiveIntegerField(default=0) # col18
    addPayIntParti = models.FloatField(default=0.00) #col19
    amtIntPart = models.FloatField(default=0.00) #col20
    totalFinalPayout = models.FloatField(default=0.00) # col21
    trp = models.FloatField(default=0.00) # col22
    addTotalFinalPayout = models.FloatField(default=0.00) # col23
    lessTDS = models.FloatField(default=0.00) # col24
    netPayout = models.FloatField(default=0.00) # col25
    imonth = models.PositiveIntegerField(default=0) # col26
    iyear = models.PositiveIntegerField(default=0) # col27
    inc_file = models.FileField(upload_to='Inc_files/', default=None, null=True)

    def __str__(self):
        return str(self.empcode)

class DoctorIncentive(models.Model):
    empcode = models.OneToOneField(EmployeeDetail, on_delete=models.CASCADE, primary_key=True)
    inc_file = models.FileField(upload_to='Inc_files/', default=None, null=True)

    def __str__(self):
        return str(self.empcode)

class DietIncentive(models.Model):
    empcode = models.OneToOneField(EmployeeDetail, on_delete=models.CASCADE, primary_key=True)
    diet_file = models.FileField(upload_to='Inc_files/', default=None, null=True)

    def __str__(self):
        return str(self.empcode)

class StaffSalaryStructure(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    empName = models.CharField(default="None", max_length=200)
    basic = models.FloatField(default=0.00)
    hra = models.FloatField(default=0.00)
    specialAll = models.FloatField(default=0.00)
    grossS = models.FloatField(default=0.00)
    start_month = models.CharField(default="None", max_length=15)
    start_year = models.PositiveIntegerField(default=0)
    end_month = models.CharField(default="None", max_length=15)
    end_year = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'StaffSalaryStructure'

    def __str__(self):
        return str(self.empcode)    

class SalaryCalculation(models.Model):
    staff_salary = models.ForeignKey(StaffSalary, on_delete=models.CASCADE)
    paid_days = models.PositiveIntegerField(default=0)
    month = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    basic_a = models.FloatField(default=0.00)
    hra_a = models.FloatField(default=0.00)
    specialAll_a = models.FloatField(default=0.00)
    grossS_a = models.FloatField(default=0.00)
    others = models.FloatField(default=0.00)
    incentive = models.FloatField(default=0.00)
    pf_deduction = models.FloatField(default=0.00)
    esic_deduction = models.FloatField(default=0.00)
    other_deduction = models.FloatField(default=0.00)
    gross_deduction = models.FloatField(default=0.00)
    income_tax = models.FloatField(default=0.00)
    netSalary = models.FloatField(default=0.00)

    def __str__(self):
        return f"{self.staff_salary.empcode} - {self.year}-{self.month}"
    

class ProfessionalSalaryCalculation(models.Model):
    id = models.AutoField(default=0,primary_key=True)
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    empName = models.TextField(default="None")
    fixPayout = models.FloatField(default=0.00)# dont use
    payDays = models.PositiveIntegerField(default=0)
    appSalary = models.FloatField(default=0.00)
    professionalFees = models.FloatField(default=0.00)
    other_earning = models.FloatField(default=0.00)
    other_deduction = models.FloatField(default=0.00)
    profIncentive = models.FloatField(default=0.00)
    grossEarn = models.FloatField(default=0.00)
    incomeT = models.FloatField(default=0.00)
    grossDed = models.FloatField(default=0.00)
    netSal = models.FloatField(default=0.00)
    month = models.CharField(default="None", max_length=15)
    year = models.PositiveIntegerField(default=0)
    class Meta :
        db_table = 'ProfessionalSalaryCalculation'
        
    def __str__(self):
        return f"{self.empcode.empcode} - {self.empName}"


class ExcerciseInce1(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE) 
    exercise_expert_name = models.CharField(default="None", max_length=250) # c1
    total_no_of_allotted_participants = models.PositiveIntegerField(default=0) #c2
    total_no_of_participants = models.PositiveIntegerField(default=0) #c3
    patients_in_red = models.PositiveIntegerField(default=0) #c4
    calling_reds = models.CharField(default='0%', max_length=10) #c5
    incentive_1 = models.PositiveIntegerField(default=0) #c6
    amount_1 = models.FloatField(default=0.00) #c7
    nps_percent = models.CharField(default='0%', max_length=10) #c8
    incentive_2 = models.PositiveIntegerField(default=0) #c9
    amount_2 = models.FloatField(default=0.00) #c10
    qrs_percent = models.CharField(default='0%', max_length=10) #c11
    incentive_3 = models.PositiveIntegerField(default=0) #c12
    amount_3 = models.FloatField(default=0.00) #c13
    total_effort_incentive = models.PositiveIntegerField(default=0) #c14
    total_effort_payout = models.FloatField(default=0.00) #c15
    vip_participants = models.PositiveIntegerField(default=0) #c16
    amount_vip_participant = models.FloatField(default=0.00) #c17
    international_participant_alloted = models.PositiveIntegerField(default=0) #c18
    add_pay_for_international_participant = models.FloatField(default=0.00) #c20
    additional_payment = models.FloatField(default=0.00) #c19
    total_effort_incentive_payout = models.FloatField(default=0.00) #c21
    trp = models.FloatField(default=0.00) #c22
    final_effort_incentive_payout = models.FloatField(default=0.00) #c23
    less_tds = models.FloatField(default=0.00) #c24
    net_payout = models.FloatField(default=0.00) #c25
    month = models.CharField(default="None", max_length=50) #c26
    year = models.PositiveIntegerField(default=0) #c27

    class Meta :
        db_table = 'ExcerciseInce1'


class DoctorInce1(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    doctor_name = models.CharField(default="None", max_length=250) #c1
    total_no_of_allotted_participants = models.PositiveIntegerField(default=0) #c2
    total_no_of_participants = models.PositiveIntegerField(default=0) #c3
    patients_in_red = models.PositiveIntegerField(default=0) #c4
    calling_reds = models.CharField(default='0%', max_length=10) #c5
    incentive_1 = models.PositiveIntegerField(default=0) #c6
    amount_1 = models.FloatField(default=0.00) #c7
    nps_percent = models.CharField(default='0%', max_length=10) #c8
    incentive_2 = models.PositiveIntegerField(default=0) #c9
    amount_2 = models.FloatField(default=0.00) #c10
    qrs_percent = models.CharField(default='0%', max_length=10) #c11
    incentive_3 = models.PositiveIntegerField(default=0) #c12
    amount_3 = models.FloatField(default=0.00) #c13
    total_effort_incentive = models.PositiveIntegerField(default=0) #c14
    total_effort_payout = models.FloatField(default=0.00) #c15
    international_participant_alloted = models.PositiveIntegerField(default=0) #c14
    add_pay_for_international_participant = models.FloatField(default=0.00) #c16
    total_effort_incentive_payout = models.FloatField(default=0.00) #c17
    trp = models.FloatField(default=0.00) #c18
    final_effort_incentive_payout = models.FloatField(default=0.00) #c19
    less_tds = models.FloatField(default=0.00) #c20
    net_payout = models.FloatField(default=0.00) #c21
    month = models.CharField(default="None", max_length=250) #c22
    year = models.PositiveIntegerField(default=0) #c23

    class Meta :
        db_table = 'DoctorInce1'


class DietInce1(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    diet_expert_name = models.CharField(default="None", max_length=250) #c1
    total_no_of_allotted_participants = models.PositiveIntegerField(default=0) #c2
    total_no_of_participants = models.PositiveIntegerField(default=0) #c3
    patients_in_red = models.PositiveIntegerField(default=0) #c4
    calling_reds = models.CharField(default='0%', max_length=10) #c5
    incentive_1 = models.PositiveIntegerField(default=0) #c6
    amount_1 = models.FloatField(default=0.00) #c7
    nps_percent = models.CharField(default='0%', max_length=10) #c8
    incentive_2 = models.PositiveIntegerField(default=0) #c9
    amount_2 = models.FloatField(default=0.00) #c10
    qrs_percent = models.CharField(default='0%', max_length=10) #c11
    incentive_3 = models.PositiveIntegerField(default=0) #c12
    amount_3 = models.FloatField(default=0.00) #c13
    total_effort_incentive = models.PositiveIntegerField(default=0) #c14
    total_effort_payout = models.FloatField(default=0.00) #c15
    vip_patients = models.PositiveIntegerField(default=0) #c14
    amount_vip_participant = models.FloatField(default=0.00) #c15
    international_participant_alloted = models.PositiveIntegerField(default=0) #c14
    add_pay_for_international_participant = models.FloatField(default=0.00) #c16
    total_effort_incentive_payout = models.FloatField(default=0.00) #c17
    less_tds = models.FloatField(default=0.00) #c20
    net_payout = models.FloatField(default=0.00) #c21
    month = models.CharField(default="None", max_length=250) #c22
    year = models.PositiveIntegerField(default=0) #c23

    class Meta :
        db_table = 'DietInce1'


class ProfessionalSalaryStructure(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    employee_name = models.CharField(default="None", max_length=250)
    app_salary = models.FloatField(default=0.00)
    professional_fees = models.FloatField(default=0.00)
    start_month = models.CharField(default="None", max_length=15)
    start_year = models.PositiveIntegerField(default=0)
    end_month = models.CharField(default="None", max_length=15)
    end_year = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ProfessionalSalaryStructure'
    

class YearlyLeaves(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    earnedLeaveT = models.PositiveIntegerField(default=36)
    earnedLeaveB = models.PositiveIntegerField(default=36)
    sickLeaveT = models.PositiveIntegerField(default=7)
    sickLeaveB = models.PositiveIntegerField(default=7)
    maternityLT = models.PositiveIntegerField(default=182)
    maternityLB = models.PositiveIntegerField(default=182)
    oH2T = models.PositiveIntegerField(default=2)
    oH2B = models.PositiveIntegerField(default=2)
    ffcT = models.PositiveIntegerField(default=4)
    ffcB = models.PositiveIntegerField(default=4)
    start_month = models.PositiveIntegerField(default=0)
    start_year = models.PositiveIntegerField(default=0)
    end_month = models.PositiveIntegerField(default=0)
    end_year = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'YearlyLeaves'
    
    def __str__(self):
        return str(self.empcode.empcode) + "-" + str(self.empcode.user.first_name) + " " + str(self.empcode.user.last_name)


class ProfessionalSalaryCal(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    empName = models.TextField(default="None")
    payDays = models.PositiveIntegerField(default=0)
    lop = models.PositiveIntegerField(default=0)
    appSalary = models.FloatField(default=0.00)
    professionalFees = models.FloatField(default=0.00)
    other_earning = models.FloatField(default=0.00)
    other_deduction = models.FloatField(default=0.00)
    profIncentive = models.FloatField(default=0.00)
    grossEarn = models.FloatField(default=0.00)
    incomeT = models.FloatField(default=0.00)
    grossDed = models.FloatField(default=0.00)
    netSal = models.FloatField(default=0.00)
    month = models.CharField(default="None", max_length=15)
    month_int = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)
    class Meta :
        db_table = 'ProfessionalSalaryCal'
        
    def __str__(self):
        return f"{self.empcode.empcode} - {self.empName}"
    

class StaffSalaryCalculation(models.Model):
    empcode = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE)
    empName = models.TextField(default="None")
    paid_days = models.PositiveIntegerField(default=0)
    lop = models.PositiveIntegerField(default=0)
    basic_a = models.FloatField(default=0.00)
    hra_a = models.FloatField(default=0.00)
    specialAll_a = models.FloatField(default=0.00)
    grossS_a = models.FloatField(default=0.00)
    others = models.FloatField(default=0.00)
    incentive = models.FloatField(default=0.00)
    pf_deduction = models.FloatField(default=0.00)
    esic_deduction = models.FloatField(default=0.00)
    professional_tax = models.FloatField(default=0.0)
    other_deduction = models.FloatField(default=0.00)
    gross_deduction = models.FloatField(default=0.00)
    income_tax = models.FloatField(default=0.00)
    netSalary = models.FloatField(default=0.00)
    month = models.CharField(default="None", max_length=15)
    month_int = models.PositiveIntegerField(default=0)
    year = models.PositiveIntegerField(default=0)

    class Meta :
        db_table = 'StaffSalaryCalculation'

    def __str__(self):
        return f"{self.empcode.empcode} - {self.year}-{self.month}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.first_name + self.user.last_name