from .models import QSUBJECT, Edit_User, ANNUAL, BTUTOR, CNAME, OVERALL_ANNUAL, TUTOR_HOME, REGISTERED_ID, ASUBJECTS
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.contrib.auth.decorators import login_required
#from result.utils import parent_id
from datetime import timedelta 
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg
#import datetime

#########################################################################################################################
start_time = time.time()
from result.utils import session
session = session()
def home_page(request, pk):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every tutor!
    """
    # If a tutor is authenticated then redirect them to the tutor's page
    if request.user.is_authenticated:#a tutor page
        tutor = BTUTOR.objects.filter(accounts=request.user, subject__exact=BTUTOR.objects.get(pk=pk).subject, Class__exact=BTUTOR.objects.get(pk=pk).Class, session__exact=BTUTOR.objects.get(pk=pk).session).order_by('term')
        return render(request, 'result/tutor.html', {'tutor':tutor})
    else:#general login page
        return redirect('logins') 

def home(request):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every tutor!
    """
    # If a tutor is authenticated then redirect them to the tutor's page
    if request.user.is_authenticated:#a tutor page
        page = TUTOR_HOME.objects.filter(tutor=request.user).order_by('id')
        return render(request, 'result/page.html', {'page':page})
    else:#general login page
        return redirect('logins')
    
    
def paginator(request, pages):
    page = request.GET.get('page', 1)
    paginator = Paginator(pages, 30)
    try:
        all_page = paginator.page(page)
    except PageNotAnInteger:
        all_page = paginator.page(1)
    except EmptyPage:
        all_page = paginator.page(paginator.num_pages)
    return all_page

def uniqueness(request, pk):
    tutor = BTUTOR.objects.get(pk=pk)
    if tutor.status == 'delete':
        BTUTOR.objects.filter(status__exact='delete').delete()
        TUTOR_HOME.objects.filter(first_term__exact=None).delete()
        return redirect('home')
    else:
        if tutor.term == '1st Term':
            tutors = TUTOR_HOME.objects.get(first_term=tutor)
            tutors.tutor = request.user
            tutors.save()
    unique = BTUTOR.objects.filter(accounts__exact=tutor.accounts, term__exact=tutor.term, Class__exact=tutor.Class, subject__exact = tutor.subject, teacher_name__exact = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session__exact = tutor.session)
    first = BTUTOR.objects.filter(accounts__exact=tutor.accounts, term__exact='1st Term', Class__exact=tutor.Class, subject__exact = tutor.subject, teacher_name__exact = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session__exact = tutor.session)
    if unique.count() > 1:
        return render(request, 'result/tutor_unique.html', {'tutor':unique, 'ids':tutor})
    elif first.count() == 0:
        others = BTUTOR.objects.filter(accounts__exact=request.user, subject__exact = tutor.subject).order_by('id')
        return render(request, 'result/first_term_record_notify.html', {'all_page':paginator(request, others), 'tutor':tutor.subject})
    else:
        return redirect('home_page', pk=pk)  

def subject_home(request, pk, cl):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every subject!
    """
    if cl == '1':#class
        detail = 'Results filtered by Class'
        tutor = BTUTOR.objects.filter(Class__exact=BTUTOR.objects.get(pk=pk).Class).order_by('session')
    elif cl == '2':#term
        detail = 'Results filtered by Term'
        tutor = BTUTOR.objects.filter(term__exact=BTUTOR.objects.get(pk=pk).term).order_by('session')
    elif cl == '3':#subject
        detail = 'Results filtered by Subject'
        tutor = BTUTOR.objects.filter(subject__exact=BTUTOR.objects.get(pk=pk).subject).order_by('session', 'Class')
    if tutor.count() != 0:    
        return render(request, 'result/tutor_class_filter.html', {'tutors':tutor, 'detail' : detail, 'counts':tutor.count()})
    else:
        return redirect('home') 
     

def subject_grade_counter(pk, md):
    from collections import Counter
    tutor = get_object_or_404(BTUTOR, pk=pk)
    if md == 'q':
        subjects = QSUBJECT.objects.filter(tutor__exact=tutor)
        count = Counter([x[0] for x in subjects.values_list('grade') if x != None])
    elif md == 'a':
        subjects = ANNUAL.objects.filter(subject_by__exact=tutor)
        count = Counter([str(x[0]) for x in subjects.values_list('Grade') if x != None])
    else:
        user = get_object_or_404(User, pk=get_object_or_404(BTUTOR, pk=pk).class_teacher_id)
        subjects = OVERALL_ANNUAL.objects.filter(teacher_in__exact=user, class_in__exact=user.profile.class_in, session__exact=session)
        count = Counter([x[0] for x in subjects.values_list('grade') if x != None])
    return sorted(count.most_common()) #[('A1', 8), ('C6', 3), ('C4', 3), ('C5', 2), ('B3', 2), ('B2', 2)]


#from result.utils import html_csv
def detailView(request, pk, md):##Step 2::  every tutor home detail views all_search_lists
    tutor = get_object_or_404(BTUTOR, pk=pk)
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('gender')#request.user 
    if mains.count() != 0 and md == '1':
        grad = subject_grade_counter(pk, 'q')
        return render(request, 'result/qsubject.html',  {'urs':mains.count(), 'grad' : grad, 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains), 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk})
    if mains.count() == 0 and md == '1':
        return redirect('upload_txt', pk=tutor.id)
    mains = ANNUAL.objects.filter(subject_by__exact=tutor).order_by('id')
    if mains.count() != 0 and md == '2':
        tutor.model_in = 'annual'
        tutor.save()
        grad = subject_grade_counter(pk, 'a')
        return render(request, 'result/all_annual.html',  {'subject_scores':round(mains.aggregate(Sum('Agr'))['Agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('Agr'))['Agr__avg'],2), 'males' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 1).count(), 'females' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains), 'qry' : tutor, 'pk': pk, 'grad': grad})
    else:
        return redirect('home')
    
def all_View(request, pk, md):##Step 2::  every tutor home detail views all_search_lists
    tutor = get_object_or_404(BTUTOR, pk=pk)
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('gender')#request.user 
    if mains.count() != 0:
        if md == '1':#scores
            grad = subject_grade_counter(pk, 'q')
            return render(request, 'result/qsubject.html',  {'grad' : grad, 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk})
        if md == '3' or md == '4' or md == '7':#males
            grad = subject_grade_counter(pk, 'q')
            mains = QSUBJECT.objects.filter(tutor__exact=tutor, gender = int(md)-2).order_by('student_name')#genders
            if md == '7':#scores pdf
                return render(request, 'result/qsubject_pdf.html',  {'all_page': QSUBJECT.objects.filter(tutor__exact=tutor).order_by('gender')})
            else:
                return render(request, 'result/qsubject.html',  {'grad' : grad, 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk})
    if mains.count() == 0 and md == '1':
        return redirect('upload_txt', pk=tutor.id)
    
    mains = ANNUAL.objects.filter(subject_by__exact=tutor).order_by('id')
    if mains.count() != 0:
        if md == '2':#annuals
            grad = subject_grade_counter(pk, 'a')
            return render(request, 'result/all_annual.html',  {'subject_scores':round(mains.aggregate(Sum('Agr'))['Agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('Agr'))['Agr__avg'],2), 'males' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 1).count(), 'females' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'qry' : tutor, 'pk': pk, 'grad': grad})
        if md == '5' or md == '6' or md == '8':
            mains = ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = int(md)-4).order_by('student_name')#ales
            grad = subject_grade_counter(pk, 'a')
            if md == '8':#annual pdf
                return render(request, 'result/all_annual_pdf.html',  {'all_page': ANNUAL.objects.filter(subject_by__exact=tutor).order_by('id')})
            else:
                return render(request, 'result/all_annual.html',  {'subject_scores':round(mains.aggregate(Sum('Agr'))['Agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('Agr'))['Agr__avg'],2), 'males' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 1).count(), 'females' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'qry' : tutor, 'pk': pk, 'grad': grad})
    else:
        return redirect('home')
#########################################################################################################################
 

@login_required   
def genders_scores(request, pk_code):##Step 2::  every tutor home detail views all_search_lists
    gender = [['a', 'b'], [1, 2]]
    tutor = get_object_or_404(BTUTOR, pk=pk_code[:-1])
    pro = get_object_or_404(Edit_User, user=request.user)
    pro.account_id = str(pk_code[:-1])+'_'+str(gender[1][gender[0].index(pk_code[-1])])
    mains = QSUBJECT.objects.filter(tutor__exact=tutor, gender = gender[1][gender[0].index(pk_code[-1])]).order_by('student_name')#request.user 
    grad = subject_grade_counter(pk_code[:-1], 'q')
    return render(request, 'result/qsubject.html',  {'grad' : grad, 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk_code[:-1]})

def annual_view_genders(request, pk_code):##Step 2::  every tutor home detail views 
    gender = [['a', 'b'], [1, 2]]
    tutor = get_object_or_404(BTUTOR, pk=pk_code[:-1])
    pro = get_object_or_404(Edit_User, user=request.user)
    pro.account_id = str(pk_code[:-1])+'_'+str(gender[1][gender[0].index(pk_code[-1])])
    pro.save()
    mains = ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = gender[1][gender[0].index(pk_code[-1])]).order_by('student_name')#request.user
    grad = subject_grade_counter(pk_code[:-1], 'a')
    return render(request, 'result/all_annual.html',  {'subject_scores':round(mains.aggregate(Sum('Agr'))['Agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('Agr'))['Agr__avg'],2), 'males' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 1).count(), 'females' : ANNUAL.objects.filter(subject_by__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'qry' : tutor, 'pk': pk_code[:-1], 'grad': grad})

def student_in_None(request):#student subject detail(single term)
    subjects = QSUBJECT.objects.filter(tutor__accounts__exact=None)
    count_grade = subjects.count()
    return render(request, 'result/qsubject_none.html',  {'all_page' : paginator(request, subjects), 'count_grade':count_grade})
       

def qsubject_on_grade(request, pk_code):##Step 2::  every tutor home detail views
    pk=pk_code.split('_')[0]
    tutor = get_object_or_404(BTUTOR, pk=pk_code.split('_')[0])
    grad = subject_grade_counter(pk, 'q')
    mains = QSUBJECT.objects.filter(tutor__exact=tutor, grade=pk_code.split('_')[1]).order_by('student_name')
    males = QSUBJECT.objects.filter(tutor__exact=tutor, grade=pk_code.split('_')[1], student_name__gender__exact = 1).count()
    females = QSUBJECT.objects.filter(tutor__exact=tutor, grade=pk_code.split('_')[1], student_name__gender__exact = 2).count()
    if mains.count() != 0:
        return render(request, 'result/qsubject.html',  {'males':males, 'females':females, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'grad' : grad, 'count_grade' : mains.count(), 'all_page': mains, 'qry' : tutor, 'pk': pk})
    else:
        return redirect('home')

def annual_on_grade(request, pk_code):##Step 2::  every tutor home detail views
    pk=pk_code.split('_')[0]
    tutor = get_object_or_404(BTUTOR, pk=pk_code.split('_')[0])
    grad = subject_grade_counter(pk, 'a')
    mains = ANNUAL.objects.filter(subject_by__exact=tutor, Grade=pk_code.split('_')[1]).order_by('student_name')
    males = ANNUAL.objects.filter(subject_by__exact=tutor, Grade=pk_code.split('_')[1], student_name__gender__exact = 1).count()
    females = ANNUAL.objects.filter(subject_by__exact=tutor, Grade=pk_code.split('_')[1], student_name__gender__exact = 2).count()
    if mains.count() != 0:
        return render(request, 'result/all_annual.html',  {'males':males, 'females':females, 'subject_scores':round(mains.aggregate(Sum('Agr'))['Agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('Agr'))['Agr__avg'],2), 'count_grade' : mains.count(), 'all_page': mains, 'qry' : tutor, 'pk': pk, 'grad': grad})
    else:
        return redirect('home')


def Student_names_list(request, pk):##Step 2::  every tutor home detail views
    gender = CNAME.objects.filter(gender__exact=pk)
    cnames = CNAME.objects.filter(pk__in=[x[0] for x in list(REGISTERED_ID.objects.filter(student_name__in=gender).values_list('student_name'))])
    mains = QSUBJECT.objects.filter(student_name__in=cnames, tutor__subject__exact=ASUBJECTS.objects.get(name='ENG'), tutor__term__exact='2nd Term').order_by('tutor')
    counted = [mains.exclude(tutor__Class__exact='JSS 1').count(), mains.exclude(tutor__Class__exact='JSS 2').count(), mains.exclude(tutor__Class__exact='JSS 3').count(), mains.exclude(tutor__Class__exact='SSS 1').count(), mains.exclude(tutor__Class__exact='SSS 2').count(), mains.exclude(tutor__Class__exact='SSS 3').count()]
    counted = [mains.count()-x for x in counted]
    return render(request, 'result/student_name_list.html',  {'all_page': paginator(request, mains), 'counts': mains.count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})


def student_on_all_subjects_list(request, pk):##Step 2::  every tutor home detail views
    
    if pk == '0':
        mains = QSUBJECT.objects.all().order_by('posi')
        tutors = len([i[0] for i in list(set(list(mains.values_list('tutor'))))])
        counts = mains.count()
        return render(request, 'result/student_on_all_subjects_list.html',  {'all_page': paginator(request, mains), 'counts': counts, 'tutors':tutors})
    else:
        tutors = BTUTOR.objects.all()
        mains = QSUBJECT.objects.all().order_by('posi')
        count_s = mains.count()
        count_t = tutors.count()
        return render(request, 'result/student_on_all_subjects_detail.html',  {'all_page': paginator(request, mains), 'count_t': count_t, 'count_s':count_s})
###    
def student_subject_list(request, pk):##Step 2::  every tutor home detail views
    mains = QSUBJECT.objects.filter(student_id=QSUBJECT.objects.get(pk=pk).student_id, tutor__session__exact=session).order_by('id')
    return render(request, 'result/student_subject_list.html',  {'all_page': paginator(request, mains), 'counts': mains.count(), 'name': QSUBJECT.objects.get(pk=pk).student_name, 'pk': pk})


def all_student_subject_list(request, pk):##Step 2::  every tutor home detail views
    mains = QSUBJECT.objects.filter(student_id=QSUBJECT.objects.get(pk=pk).student_id, tutor__session__exact=session)
    return render(request, 'result/all_student_subject_list.html',  {'mains': mains, 'counts': mains.count(), 'name': QSUBJECT.objects.get(pk=pk).student_name, 'pk': pk, 'cnt': pk})

##########################PORTAL MANAGEMENT#################################### 


def teacher_accounts(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/transfers.html', {'all_page': paginator(request, tutors), 'counts':tutors.count()})

def all_teachers(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/all_transfers.html', {'tutors': tutors, 'counts':tutors.count()})

def home_page_return(request, pk):
    tutor = BTUTOR.objects.get(pk=pk)
    if tutor.term == '1st Term':
        tutors = TUTOR_HOME.objects.get(first_term = tutor)
        tutors.first_term = QSUBJECT.objects.get(tutor = tutor).tutor
        tutors.save()
    elif tutor.term == '2nd Term':
        tutors = TUTOR_HOME.objects.get(second_term = tutor)
        tutors.second_term = QSUBJECT.objects.get(tutor = tutor).tutor
        tutor.save()
    else:
        tutors = TUTOR_HOME.objects.get(third_term = tutor)
        tutors.third_term = QSUBJECT.objects.get(tutor = tutor).tutor
        tutors.save()


def results_junior_senior(request, pk):
    cls = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']
    tutors = BTUTOR.objects.filter(Class__exact=cls[int(pk)]).exclude(accounts__exact=None).order_by('term')
    return render(request, 'result/results_junior_senior.html', {'all_page': paginator(request, tutors), 'pk':pk, 'counts':tutors.count()})
  
    

def once_results_junior_senior(request, pk):
    cls = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']
    tutors = BTUTOR.objects.filter(Class__exact=cls[int(pk)]).exclude(accounts__exact=None).order_by('term')
    return render(request, 'result/all_results_junior_senior.html', {'tutor': tutors, 'pk':pk, 'counts':tutors.count()})

def all_users(request):#show single candidate profile
    qry = User.objects.all()
    return render(request, 'result/all_users.html', {'qry' : qry})

def student_subject_detail_one_subject(request, pk):#student subject detail(single term)
    many = get_object_or_404(QSUBJECT, pk=pk)
    subjects = QSUBJECT.objects.filter(student_name = many.student_name, tutor__subject__exact=many.tutor.subject)
    anuual = subjects.aggregate(Sum('agr'))['agr__sum']
    elapsed_time_secs = time.time() - start_time
    msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
    print(msg)
    return render(request, 'result/single_subject_per_student.html',  {'subjects' : subjects, 'name':many, 'anuual':anuual, 'pk':pk}) 

def student_subject_detail_all_subject(request, pk):#student subject detail(single term)
    many = get_object_or_404(QSUBJECT, pk=pk)
    subjects = QSUBJECT.objects.filter(student_name = many.student_name, tutor__Class__exact=many.tutor.Class)
    anuual = subjects.aggregate(Sum('agr'))['agr__sum']
    elapsed_time_secs = time.time() - start_time
    msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
    print(msg)
    return render(request, 'result/single_subject_per_student.html',  {'subjects' : subjects, 'name':many, 'anuual':anuual, 'pk':pk}) 

def searchs(request):
    query = request.GET.get("q")
    reg = REGISTERED_ID.objects.filter(student_name__in=CNAME.objects.filter(last_name__icontains = query.upper()), session__exact=session)
    return render(request, 'result/searched_names.html',  {'all_page' : reg}) 	

def search_results(request, pk):
        redir = [x[0] for x in list(QSUBJECT.objects.filter(student_id=REGISTERED_ID.objects.get(pk=pk).student_id).values_list('id'))]
        return redirect('student_subject_list', pk=redir[0])
    
def broad_sheet_views(request, pk):
    start_time = time.time()
    from .explorer import subject_counter
    al = OVERALL_ANNUAL.objects.filter(class_in__exact=BTUTOR.objects.get(pk=pk).Class, session__exact=session)  
    elapsed_time_secs = time.time() - start_time
    msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
    print(msg)
    if al.count() !=  0:
        if BTUTOR.objects.get(pk=pk).Class == 'JSS 1' or BTUTOR.objects.get(pk=pk).Class == 'JSS 2' or BTUTOR.objects.get(pk=pk).Class == 'JSS 3':
            return render(request, 'result/jyearly.html',  {'msg':msg, 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2),'all_page': paginator(request, al), 'class_in':BTUTOR.objects.get(pk=pk).Class, 'counts':al.count()})
        else:
            return render(request, 'result/syearly.html',  {'msg':msg, 'sct':subject_counter(request), 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2), 'all_page': paginator(request, al), 'class_in':BTUTOR.objects.get(pk=pk).Class, 'counts':al.count()})
    else:
        return redirect('home')
    
	

    