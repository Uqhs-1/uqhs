from django.contrib import admin
from .models import ASUBJECTS, BTUTOR, CNAME, QSUBJECT, ANNUAL, Edit_User, OVERALL_ANNUAL, SESSION, REGISTERED_ID, STUDENT_INFO, QUESTION, STUDENT
#admin.site.register(studen_scores)#
########################################################
# Define the admin class
class subject_main(admin.ModelAdmin):
    list_display = ('student_name', 'gender', 'cader', 'tutor', 'info', 'term')
    fields = [('student_name', 'gender', 'cader', 'student_id'), ('test', 'agn', 'atd', 'total', 'exam', 'agr'), ('grade', 'posi'),('tutor', 'master_comment', 'principal_comment', 'resumption')]#, 'subject']

@admin.register(BTUTOR)
class model_teacher(admin.ModelAdmin):
    list_display = ('model_in','accounts', 'cader', 'teacher_name', 'subject', 'Class', 'term', 'model_summary', 'session')
    fields = [('cader', 'model_in','accounts', 'teacher_name'), ('subject', 'Class', 'term'), ('model_summary', 'session', 'resumption')]

@admin.register(OVERALL_ANNUAL)
class model_qsubject(admin.ModelAdmin):
    list_display = ('order', 'student_name','class_in', 'eng', 'mat', 'bus', 'bst', 'yor', 'nva', 'irs', 'prv', 'ict', 'agr', 'his', 'AGR', 'AVR', 'GRD', 'POS')
    fields = [('student_name','class_in'), ('eng', 'mat', 'bus', 'bst', 'yor', 'nva', 'irs', 'prv', 'ict', 'agr', 'his'), ('AGR', 'AVR', 'GRD', 'POS')]

@admin.register(ANNUAL)
class model_annual(admin.ModelAdmin):
    list_display = ('id', 'student_name', 'first', 'second', 'third', 'anual', 'Agr', 'Grade', 'Posi', 'subject_by')
    fields = ['student_name', ('first', 'second', 'third', 'summary', 'anual'), ('Agr', 'Grade', 'Posi'), 'subject_by']
@admin.register(CNAME)
class model_names(admin.ModelAdmin):
    list_display = ('id', 'gender', 'last_name', 'first_name', 'full_name', 'created', 'updated')
    fields = [('last_name', 'first_name', 'full_name'), ('gender', 'birth_date')]
    
@admin.register(REGISTERED_ID)
class model_ids(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'student_class', 'session')
    fields = [('student_name', 'student_class'), ('student_id', 'session')]
@admin.register(Edit_User)
class model_profile(admin.ModelAdmin):
    list_display = ('title', 'user', 'account_id', 'photo','phone', 'city', 'country', 'organization', 'location', 'birth_date', 'department')
    fields = [('title', 'user', 'account_id'), ('photo', 'image'), 'bio', ('phone', 'city', 'country', 'organization', 'location', 'birth_date', 'department'), 'email_confirmed']

@admin.register(QUESTION)
class model_QUESTION(admin.ModelAdmin):
    list_display = ('serial_no','subjects', 'classes', 'terms', 'questNum', 'updated')
    fields = [('subjects', 'classes', 'terms', 'questNum', 'CORRECT'), ('question', 'photo', 'image'), ('optionA', 'optionB', 'optionC', 'optionD'), ('answerA', 'answerB', 'answerC', 'answerD'), 'comment']
@admin.register(STUDENT_INFO)
class model_student_info(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'no_open', 'no_present', 'no_absent', 'comment', 'H_begin', 'H_end', 'W_begin', 'W_end', 'no_of_day_abs', 'purpose', 'good', 'fair', 'poor', 'remark', 'event', 'indoor', 'ball', 'combat', 'track', 'jump', 'throw', 'swim', 'lift', 'sport_comment', 'club_one', 'club_two', 'office_one', 'office_two', 'contrib_one', 'contrib_two')
    fields = [('student_id', 'student_name'), ('no_open', 'no_present', 'no_absent', 'comment'), ('H_begin', 'H_end', 'W_begin', 'W_end', 'no_of_day_abs', 'purpose'), ('good', 'fair', 'poor', 'remark'), ('event', 'indoor', 'ball', 'combat', 'track', 'jump', 'throw', 'swim', 'lift', 'sport_comment'), ('club_one', 'club_two', 'office_one', 'office_two', 'contrib_one', 'contrib_two')]


admin.site.register(STUDENT)
admin.site.register(ASUBJECTS)
admin.site.register(SESSION)
admin.site.register(QSUBJECT, subject_main)#second_term
# Register your models here.
