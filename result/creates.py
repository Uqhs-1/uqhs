from .models import QSUBJECT, ASUBJECTS, BTUTOR, TUTOR_HOME
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import subjectforms, subject_class_term_Form, sessions, FORMARTS
from django.contrib.auth.decorators import login_required
from result.utils import cader, session



session = session()

def create_subjects(request):#New teacher form for every new term, class, subjects
    if request.method == 'POST':
        result = subjectforms(request.POST)
        if result.is_valid():
            check = ASUBJECTS.objects.filter(name__exact=result.cleaned_data['name'])
            if len(check) == 0: 
                new_subject = ASUBJECTS(name=result.cleaned_data['name'])
                new_subject.save()
                return redirect('teacher_create')
            else:
                check = ASUBJECTS.objects.all().order_by('id')
                return render(request, 'result/created_subject.html', {'check' : check})
    else:
        result = subjectforms()
    return render(request, 'result/create_new_subject.html', {'result': result})
#########################################################
def created_subjects(request, pk):#New teacher form for every new term, class, subjects 
    if pk == '0':
        check = ASUBJECTS.objects.all().order_by('id')
        return render(request, 'result/created_subject.html', {'check':check})
        
    else:
        SUB_NAME = ASUBJECTS.objects.get(pk=pk)
        subject = QSUBJECT.objects.filter(tutor__subject__exact=ASUBJECTS.objects.get(pk=pk)).order_by('id')
        count_grade = QSUBJECT.objects.filter(tutor__subject__exact=ASUBJECTS.objects.get(pk=pk)).count()
    page = request.GET.get('page', 1)
    paginator = Paginator(subject, 30)
    try:
        all_page = paginator.page(page)
    except PageNotAnInteger:
        all_page = paginator.page(1)
    except EmptyPage:
        all_page = paginator.page(paginator.num_pages)
    return render(request, 'result/subject_in_all.html',  {'count_grade' : count_grade, 'all_page': all_page, 'pk' : pk, 'SUB_NAME':SUB_NAME})


@login_required
def create_new_subject_teacher(request):# teacher form for every new term, class, subjects, subject_per_name
    if request.method == 'POST':
        result = subject_class_term_Form(request.POST)
        if result.is_valid():
            unique = BTUTOR.objects.filter(accounts__exact=request.user, term__exact='1st Term', Class__exact=result.cleaned_data['Class'], subject__exact = result.cleaned_data['subject'], teacher_name__exact = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session__exact = session).count()
            if unique == 0:
                new_teacher = BTUTOR(accounts=request.user, subject = result.cleaned_data['subject'], Class = result.cleaned_data['Class'], term = '1st Term', cader=cader(result.cleaned_data['Class']), teacher_name = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session = session)
                new_teacher.save()
                TUTOR_HOME(tutor=request.user, teacher_name = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', first_term = new_teacher).save()
                return redirect('upload_txt', pk=new_teacher.id)
            else:
                others = BTUTOR.objects.filter(accounts__exact=request.user, subject__exact = result.cleaned_data['subject']).order_by('id')
                page = request.GET.get('page', 1)
                paginator = Paginator(others, 30)
                try:
                    all_page = paginator.page(page)
                except PageNotAnInteger:
                    all_page = paginator.page(1)
                except EmptyPage:
                    all_page = paginator.page(paginator.num_pages)
                return render(request, 'result/first_term_record_notify.html', {'all_page':all_page, 'tutor':result.cleaned_data['subject']})
    else:
        result = subject_class_term_Form()
        return render(request, 'result/create_new_teacher.html', {'result': result})

def update_teacher_class(request, pk, tr):
    previous = TUTOR_HOME.objects.get(first_term=BTUTOR.objects.get(pk=pk))
    term = ['1st Term', '2nd Term', '3rd Term'][int(tr)]
    if BTUTOR.objects.filter(accounts__exact=request.user, subject__exact = previous.first_term.subject, Class__exact = previous.first_term.Class, term__exact = term, cader__exact=cader(previous.first_term.Class), teacher_name__exact = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session = session).count() == 0:
        new_term = BTUTOR(accounts=request.user, subject = previous.first_term.subject, Class = previous.first_term.Class, term = term, cader=cader(previous.first_term.Class), teacher_name = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session = session)
        new_term.save()
        if term == '2nd Term':
            previous.second_term = new_term
        else:
            if term == '3rd Term':
                previous.third_term = new_term
        previous.save()
        pk = new_term.id
    if term == '3rd Term' and BTUTOR.objects.filter(accounts__exact=request.user, subject__exact = previous.first_term.subject, Class__exact = previous.first_term.Class, term__in = ['1st Term', '2nd Term'], cader__exact=cader(previous.first_term.Class), teacher_name__exact = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session = session).count() == 1:
        return redirect('home')
    return redirect('upload_txt', pk=pk)

def search_pdf(request):
    if request.method == 'POST':
        form = subject_class_term_Form(request.POST)
        subject = subjectforms(request.POST)
        new = sessions(request.POST)
        frmt = FORMARTS(request.POST)
        if form.is_valid() and new.is_valid() and subject.is_valid() and frmt.is_valid():
            xv = [['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'], ['ACC', 'AGR', 'ARB', 'BST', 'BIO', 'BUS', 'CTR', 'CHE', 'CIV', 'COM', 'ECO', 'ELE', 'ENG', 'FUR', 'GRM', 'GEO', 'GOV', 'HIS', 'ICT', 'IRS', 'LIT', 'MAT', 'NAV', 'PHY', 'PRV', 'YOR', None], ['1st Term', '2nd Term', '3rd Term', None]]
            return redirect('past_csvs', Class=xv[0].index(form.cleaned_data['Class']), subject=xv[1].index(subject.cleaned_data['name']), term=xv[2].index(form.cleaned_data['term']), session=new.cleaned_data['new'], formats=frmt.cleaned_data['formats'])
    else:
        form = subject_class_term_Form()
        subject = subjectforms()
        new = sessions()
        frmt = FORMARTS()
    return render(request, 'result/past_pdf.html', {'form': form, 'new': new, 'subject':subject, 'frmt':frmt})