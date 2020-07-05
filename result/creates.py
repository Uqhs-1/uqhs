from .models import QSUBJECT, ASUBJECTS, BTUTOR, TUTOR_HOME
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import subjectforms, subject_class_term_Form, sessions, FORMARTS, class_term
from django.contrib.auth.decorators import login_required
from .utils import cader, session

def create_new_subject_teacher(request, Subject, Class, Term): #if not exist.exists():
        if Subject == 'BST 1' or Subject == 'BST 2':
            Subject = 'BST'
        new_subject = ASUBJECTS.objects.filter(name=Subject).first()
        if not ASUBJECTS.objects.filter(name__exact=Subject).exists():
            new_subject = ASUBJECTS(name=Subject)
            new_subject.save()
        new_teacher = BTUTOR(accounts=request.user, subject = new_subject, Class = Class, term = Term, first_term = Term, model_in = 'qsubject', cader=cader(Class), teacher_name = f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}', session = session())
        new_teacher.save()
        tutors = TUTOR_HOME(tutor = new_teacher.accounts, first_term = new_teacher)
        tutors.save()
        return new_teacher

def search_pdf(request):
    if request.method == 'POST':
        form = class_term(request.POST)
        subject = subjectforms(request.POST)
        new = sessions(request.POST)
        frmt = FORMARTS(request.POST)
        if form.is_valid() and new.is_valid() and subject.is_valid() and frmt.is_valid():
            xv = [['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'], ['ACC', 'AGR', 'ARB', 'BST', 'BIO', 'BUS', 'CTR', 'CHE', 'CIV', 'COM', 'ECO', 'ELE', 'ENG', 'FUR', 'GRM', 'GEO', 'GOV', 'HIS', 'ICT', 'IRS', 'LIT', 'MAT', 'NAV', 'PHY', 'PRV', 'YOR', None], ['1st Term', '2nd Term', '3rd Term', None]]
            return redirect('past_csvs', Class=xv[0].index(form.cleaned_data['Class']), subject=xv[1].index(subject.cleaned_data['name']), term=xv[2].index(form.cleaned_data['term']), session=new.cleaned_data['new'], formats=frmt.cleaned_data['formats'])
    else:
        form = class_term()
        subject = subjectforms()
        new = sessions()
        frmt = FORMARTS()
    return render(request, 'result/past_pdf.html', {'form': form, 'new': new, 'subject':subject, 'frmt':frmt})


