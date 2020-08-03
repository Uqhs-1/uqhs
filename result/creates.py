from .models import QSUBJECT, ASUBJECTS, BTUTOR, TUTOR_HOME
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

