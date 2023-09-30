from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources
from import_export.results import RowResult
#---
from django.contrib.auth.admin import UserAdmin
#---
admin.site.register(Profile)
#admin.site.register(EmployeeDetail)
#admin.site.register(Attendance)
admin.site.register(Attend)
admin.site.register(ApplyForLeave)
admin.site.register(AttendanceSummary)
#admin.site.register(StaffSalary)
#admin.site.register(Incentive)
#admin.site.register(DoctorIncentive)
#admin.site.register(DietIncentive)
#admin.site.register(SalaryCalculation)
admin.site.register(YearlyLeaves)
#----
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['id','username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
#----

class EmployeeDetailResource(resources.ModelResource):
    class Meta:
        model = EmployeeDetail
        #skip_unchanged = True
        #report_skipped = False
        fields = (
            'empcode','user','empdept', 'designation', 'contact', 'gender', 'joiningDate',
            'manage', 'dob', 'adhar', 'pfno', 'uan', 'esicip', 'bank', 'ifsc', 'accountno', 
            'emptype', 'leavingDate', 'status', 'company_name'
        
    )
        import_id_fields = ('empcode','contact')  # Map to the column name in your CSV

@admin.register(EmployeeDetail)
class EmployeeDetailData(ImportExportModelAdmin):  # Use ImportExportModelAdmin
    resource_class = EmployeeDetailResource
    list_display = (
        'empcode', 'user','empdept', 'designation', 'contact', 'gender', 'joiningDate',
        'manage', 'dob', 'adhar', 'pfno', 'uan', 'esicip', 'bank', 'ifsc', 'accountno', 
        'emptype', 'leavingDate', 'status', 'company_name'
    )
    

    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        if data.get(field.column_name) is None:
            if field.column_name == 'dob':
                data[field.column_name] = '-'
            elif field.column_name == 'adhar':
                data[field.column_name] = '-'
            elif field.column_name == 'pfno':
                data[field.column_name] = 'Not Applicable'
            elif field.column_name == 'uan':
                data[field.column_name] = 'Not Applicable'
            elif field.column_name == 'esicip':
                data[field.column_name] = 'Not Applicable'
            elif field.column_name == 'bank':
                data[field.column_name] = '-'
            elif field.column_name == 'ifsc':
                data[field.column_name] = '-'
            elif field.column_name == 'accountno':
                data[field.column_name] = '-'
            elif field.column_name == 'leavingDate':
                data[field.column_name] = '-'
            
            # Handle other fields similarly

        return super().import_field(field, obj, data, is_m2m)

'''
class ProfessionalSalaryCalculationResource(resources.ModelResource):
    class Meta:
        model = ProfessionalSalaryCalculation
        #skip_unchanged = True
        #report_skipped = False
        fields = (
        'empcode', 'empName', 'fixPayout', 'payDays',
        'appSalary', 'professionalFees', 'month', 'year'
    )
        import_id_fields = ('empcode',)  # Map to the column name in your CSV

@admin.register(ProfessionalSalaryCalculation)
class ProfessionalData(ImportExportModelAdmin):  # Use ImportExportModelAdmin
    resource_class = ProfessionalSalaryCalculationResource
    list_display = (
        'empcode', 'empName', 'fixPayout', 'payDays',
        'appSalary', 'professionalFees', 'other_earning', 'other_deduction', 'profIncentive', 'grossEarn', 'incomeT', 'grossDed', 'netSal',  'month', 'year'
    )
    

    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        if data.get(field.column_name) is None:
            if field.column_name == 'professionalFees':
                data[field.column_name] = 0.00
            elif field.column_name == 'payDays':
                data[field.column_name] = 0
            # Handle other fields similarly

        return super().import_field(field, obj, data, is_m2m)
'''

class ExcerciseIncentiveResource(resources.ModelResource):
    class Meta:
        model = ExcerciseInce1
        fields = (
            'empcode', 'exercise_expert_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds', 'incentive_1',
            'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 
            'total_effort_incentive', 'total_effort_payout', 'vip_participants', 'amount_vip_participant',
            'international_participant_alloted',  'add_pay_for_international_participant','additional_payment', 'total_effort_incentive_payout', 'trp',
            'final_effort_incentive_payout', 'less_tds', 'net_payout', 'month', 'year'
        )
        import_id_fields = ('empcode','month', 'year') # Map to the column name in your CSV

@admin.register(ExcerciseInce1)
class ExcerciseIncentiveData(ImportExportModelAdmin):
    resource_class = ExcerciseIncentiveResource
    list_display = (
            'empcode', 'exercise_expert_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds', 'incentive_1',
            'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 
            'total_effort_incentive', 'total_effort_payout', 'vip_participants', 'amount_vip_participant',
            'international_participant_alloted', 'add_pay_for_international_participant','additional_payment', 'total_effort_incentive_payout', 'trp',
            'final_effort_incentive_payout', 'less_tds', 'net_payout', 'month', 'year'
        )
    
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        month = data.get('month')
        year = data.get('year')
        existing_entry = ExcerciseInce1.objects.filter(empcode=empcode, month=month, year=year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = ExcerciseInce1(empcode=empcode, month=month, year=year)
            obj.save()  # Create a new entry
        if data.get(field.column_name) is None:
            if field.column_name == 'exercise_expert_name':
                data[field.column_name] = "None"
            elif field.column_name == 'total_no_of_allotted_participants':
                data[field.column_name] = 0
            elif field.column_name == 'total_no_of_participants':
                data[field.column_name] = 0
            elif field.column_name == 'patients_in_red':
                data[field.column_name] = 0
            elif field.column_name == 'calling_reds':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_1':
                data[field.column_name] = 0
            elif field.column_name == 'amount_1':
                data[field.column_name] = 0.00
            elif field.column_name == 'nps_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_2':
                data[field.column_name] = 0
            elif field.column_name == 'amount_2':
                data[field.column_name] = 0.00
            elif field.column_name == 'qrs_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_3':
                data[field.column_name] = 0
            elif field.column_name == 'amount_3':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive':
                data[field.column_name] = 0
            elif field.column_name == 'total_effort_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'vip_participants':
                data[field.column_name] = 0
            elif field.column_name == 'amount_vip_participant':
                data[field.column_name] = 0.00
            elif field.column_name == 'international_participant_alloted':
                data[field.column_name] = 0
            elif field.column_name == 'add_pay_for_international_participant':
                data[field.column_name] = 0.00
            elif field.column_name == 'additional_payment':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'trp':
                data[field.column_name] = 0.00
            elif field.column_name == 'final_effort_incentive_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'less_tds':
                data[field.column_name] = 0.00
            elif field.column_name == 'net_payout':
                data[field.column_name] = 0.00
            
            # Handle other fields similarly

        return super().import_field(field, obj, data, is_m2m)
    

class DoctorIncentiveResource(resources.ModelResource):
    class Meta:
        model = DoctorInce1
        fields = (
            'empcode', 'doctor_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds',
            'incentive_1', 'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 'total_effort_incentive',
            'total_effort_payout', 'international_participant_alloted', 'add_pay_for_international_participant', 'total_effort_incentive_payout', 'trp', 'final_effort_incentive_payout',
            'less_tds', 'net_payout', 'month', 'year'
        )
        import_id_fields = ('empcode','month', 'year') # Map to the column name in your CSV

@admin.register(DoctorInce1)
class DoctorIncentiveData(ImportExportModelAdmin):
    resource_class = DoctorIncentiveResource
    list_display = (
            'empcode', 'doctor_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds',
            'incentive_1', 'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 'total_effort_incentive',
            'total_effort_payout', 'international_participant_alloted', 'add_pay_for_international_participant', 'total_effort_incentive_payout', 'trp', 'final_effort_incentive_payout',
            'less_tds', 'net_payout', 'month', 'year'
        )
    
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        month = data.get('month')
        year = data.get('year')
        existing_entry = DoctorInce1.objects.filter(empcode=empcode, month=month, year=year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = DoctorInce1(empcode=empcode, month=month, year=year)
            obj.save()  # Create a new entry
        if data.get(field.column_name) is None:
            if field.column_name == 'doctor_name':
                data[field.column_name] = "None"
            elif field.column_name == 'total_no_of_allotted_participants':
                data[field.column_name] = 0
            elif field.column_name == 'total_no_of_participants':
                data[field.column_name] = 0
            elif field.column_name == 'patients_in_red':
                data[field.column_name] = 0
            elif field.column_name == 'calling_reds':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_1':
                data[field.column_name] = 0
            elif field.column_name == 'amount_1':
                data[field.column_name] = 0.00
            elif field.column_name == 'nps_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_2':
                data[field.column_name] = 0
            elif field.column_name == 'amount_2':
                data[field.column_name] = 0.00
            elif field.column_name == 'qrs_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_3':
                data[field.column_name] = 0
            elif field.column_name == 'amount_3':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive':
                data[field.column_name] = 0
            elif field.column_name == 'total_effort_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'international_participant_alloted':
                data[field.column_name] = 0
            elif field.column_name == 'add_pay_for_international_participant':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'trp':
                data[field.column_name] = 0.00
            elif field.column_name == 'final_effort_incentive_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'less_tds':
                data[field.column_name] = 0.00
            elif field.column_name == 'net_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'month':
                data[field.column_name] = "None"
            elif field.column_name == 'year':
                data[field.column_name] = 0
        
        return super().import_field(field, obj, data, is_m2m)


class DietIncentiveResource(resources.ModelResource):
    class Meta:
        model = DietInce1
        fields = (
            'empcode', 'diet_expert_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds',
            'incentive_1', 'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 'total_effort_incentive',
            'total_effort_payout', 'vip_patients', 'amount_vip_participant', 'international_participant_alloted', 'add_pay_for_international_participant', 'total_effort_incentive_payout', 
            'less_tds', 'net_payout', 'month', 'year'
        )
        import_id_fields = ('empcode','month', 'year') # Map to the column name in your CSV

@admin.register(DietInce1)
class DietIncentiveData(ImportExportModelAdmin):
    resource_class = DietIncentiveResource
    list_display = (
            'empcode', 'diet_expert_name', 'total_no_of_allotted_participants', 'total_no_of_participants', 'patients_in_red', 'calling_reds',
            'incentive_1', 'amount_1', 'nps_percent', 'incentive_2', 'amount_2', 'qrs_percent', 'incentive_3', 'amount_3', 'total_effort_incentive',
            'total_effort_payout', 'vip_patients', 'amount_vip_participant', 'international_participant_alloted', 'add_pay_for_international_participant', 'total_effort_incentive_payout', 
            'less_tds', 'net_payout', 'month', 'year'
        )
    
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        month = data.get('month')
        year = data.get('year')
        existing_entry = DietInce1.objects.filter(empcode=empcode, month=month, year=year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = DietInce1(empcode=empcode, month=month, year=year)
            obj.save()  # Create a new entry
        if data.get(field.column_name) is None:
            if field.column_name == 'diet_expert_name':
                data[field.column_name] = "None"
            elif field.column_name == 'total_no_of_allotted_participants':
                data[field.column_name] = 0
            elif field.column_name == 'total_no_of_participants':
                data[field.column_name] = 0
            elif field.column_name == 'patients_in_red':
                data[field.column_name] = 0
            elif field.column_name == 'calling_reds':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_1':
                data[field.column_name] = 0
            elif field.column_name == 'amount_1':
                data[field.column_name] = 0.00
            elif field.column_name == 'nps_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_2':
                data[field.column_name] = 0
            elif field.column_name == 'amount_2':
                data[field.column_name] = 0.00
            elif field.column_name == 'qrs_percent':
                data[field.column_name] = '0%'
            elif field.column_name == 'incentive_3':
                data[field.column_name] = 0
            elif field.column_name == 'amount_3':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive':
                data[field.column_name] = 0
            elif field.column_name == 'total_effort_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'vip_patients':
                data[field.column_name] = 0
            elif field.column_name == 'amount_vip_participant':
                data[field.column_name] = 0.00
            elif field.column_name == 'international_participant_alloted':
                data[field.column_name] = 0
            elif field.column_name == 'add_pay_for_international_participant':
                data[field.column_name] = 0.00
            elif field.column_name == 'total_effort_incentive_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'less_tds':
                data[field.column_name] = 0.00
            elif field.column_name == 'net_payout':
                data[field.column_name] = 0.00
            elif field.column_name == 'month':
                data[field.column_name] = "None"
            elif field.column_name == 'year':
                data[field.column_name] = 0
        
        return super().import_field(field, obj, data, is_m2m)


class ProfessionalSalaryStructureResource(resources.ModelResource):
    class Meta:
        model = ProfessionalSalaryStructure
        fields = (
            'empcode', 'employee_name', 'app_salary', 'professional_fees', 'start_month', 'start_year',
             'end_month', 'end_year'
        )
        import_id_fields = ('empcode','start_month', 'start_year', 'end_month', 'end_year')# Map to the column name in your CSV

@admin.register(ProfessionalSalaryStructure)
class ProfessionalSalaryStructureData(ImportExportModelAdmin):
    resource_class = ProfessionalSalaryStructureResource
    list_display = (
             'empcode', 'employee_name', 'app_salary', 'professional_fees', 'start_month', 'start_year',
             'end_month', 'end_year'
        )
    
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        start_month = data.get('start_month')
        start_year = data.get('start_year')
        end_month = data.get('end_month')
        end_year = data.get('end_year')

        existing_entry = ProfessionalSalaryStructure.objects.filter(empcode=empcode, start_month=start_month, start_year=start_year, end_month=end_month, end_year=end_year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = ProfessionalSalaryStructure(empcode=empcode, start_month=start_month, start_year=start_year, end_month=end_month, end_year=end_year)
            obj.save()  # Create a new entry
        if data.get(field.column_name) is None:
            if field.column_name == 'employee_name':
                data[field.column_name] = "None"
            
        
        return super().import_field(field, obj, data, is_m2m)

class ProfessionalSalaryCalResource(resources.ModelResource):
    class Meta:
        model = ProfessionalSalaryCal
        #skip_unchanged = True
        #report_skipped = False
        fields = (
        'empcode', 'empName', 'lop', 'other_earning', 'other_deduction', 'month', 'year'
    )
        import_id_fields = ('empcode','month', 'year')  # Map to the column name in your CSV

@admin.register(ProfessionalSalaryCal)
class ProfessionalData(ImportExportModelAdmin):  # Use ImportExportModelAdmin
    resource_class = ProfessionalSalaryCalResource
    list_display = (
        'empcode', 'empName', 'payDays', 'lop',
        'appSalary', 'professionalFees', 'other_earning', 'other_deduction', 'profIncentive', 'grossEarn', 'incomeT', 'grossDed', 'netSal',  'month', 'year'
    )
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        month = data.get('month')
        year = data.get('year')
        existing_entry = ProfessionalSalaryCal.objects.filter(empcode=empcode, month=month, year=year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = ProfessionalSalaryCal(empcode=empcode, month=month, year=year)
            obj.save()  # Create a new entry

    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        if data.get(field.column_name) is None:
            if field.column_name == 'lop':
                data[field.column_name] = 0
            elif field.column_name == 'empName':
                data[field.column_name] = "None"
            elif field.column_name == 'other_earning':
                data[field.column_name] = 0.00
            elif field.column_name == 'other_deduction':
                data[field.column_name] = 0.00
            
            # Handle other fields similarly

        return super().import_field(field, obj, data, is_m2m)


class StaffSalaryStructureResource(resources.ModelResource):
    class Meta:
        model = StaffSalaryStructure
        fields = (
            'empcode', 'empName', 'basic', 'hra', 'specialAll', 'grossS','start_month', 'start_year',
             'end_month', 'end_year'
        )
        import_id_fields = ('empcode','start_month', 'start_year', 'end_month', 'end_year')# Map to the column name in your CSV

@admin.register(StaffSalaryStructure)
class StaffSalaryStructureData(ImportExportModelAdmin):
    resource_class = StaffSalaryStructureResource
    list_display = (
             'empcode', 'empName', 'basic', 'hra', 'specialAll', 'grossS','start_month', 'start_year',
             'end_month', 'end_year'
        )
    
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        start_month = data.get('start_month')
        start_year = data.get('start_year')
        end_month = data.get('end_month')
        end_year = data.get('end_year')

        existing_entry = ProfessionalSalaryStructure.objects.filter(empcode=empcode, start_month=start_month, start_year=start_year, end_month=end_month, end_year=end_year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = ProfessionalSalaryStructure(empcode=empcode, start_month=start_month, start_year=start_year, end_month=end_month, end_year=end_year)
            obj.save()  # Create a new entry
            
        
        return super().import_field(field, obj, data, is_m2m)


class StaffSalaryCalculationResource(resources.ModelResource):
    class Meta:
        model = StaffSalaryCalculation
        #skip_unchanged = True
        #report_skipped = False
        fields = (
        'empcode', 'empName', 'lop', 'others', 'incentive', 'other_deduction', 'month', 'year'
    )
        import_id_fields = ('empcode','month', 'year')  # Map to the column name in your CSV

@admin.register(StaffSalaryCalculation)
class StaffCalculationData(ImportExportModelAdmin):  # Use ImportExportModelAdmin
    resource_class = StaffSalaryCalculationResource
    list_display = (
        'empcode', 'empName', 'paid_days', 'lop', 'basic_a', 'hra_a', 'specialAll_a', 'grossS_a', 'others', 'incentive', 'pf_deduction',
	'esic_deduction', 'professional_tax', 'other_deduction', 'gross_deduction', 'income_tax', 'netSalary', 'month', 'year'
    )
    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        empcode = data.get('empcode')
        month = data.get('month')
        year = data.get('year')
        existing_entry = StaffSalaryCalculation.objects.filter(empcode=empcode, month=month, year=year).first()

        if existing_entry:
            obj = existing_entry  # Update the existing entry
        else:
            obj = StaffSalaryCalculation(empcode=empcode, month=month, year=year)
            obj.save()  # Create a new entry

    # Customize how to handle missing values
    def import_field(self, field, obj, data, is_m2m=False):
        if data.get(field.column_name) is None:
            if field.column_name == 'lop':
                data[field.column_name] = 0
            elif field.column_name == 'empName':
                data[field.column_name] = "None"
            elif field.column_name == 'others':
                data[field.column_name] = 0.00
            elif field.column_name == 'other_deduction':
                data[field.column_name] = 0.00
            elif field.column_name == 'incentive':
                data[field.column_name] = 0.00
            
            # Handle other fields similarly

        return super().import_field(field, obj, data, is_m2m)