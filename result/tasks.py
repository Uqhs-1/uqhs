# in any app that you want celery tasks, make a tasks.py and the celery app will autodiscover that file and those tasks.
from __future__ import absolute_import
from celery import shared_task
from django.contrib.auth.models import User
from .utils import session, Render 
from .models import CNAME, BTUTOR, QSUBJECT
session = session()
from .views import param_cards, param_marksheets
from celery.decorators import task 

myHod = User.objects.filter(profile__class_in__exact='HEADS')
#@shared_task
@task(name="generate cards/marksheet")
def zipped_my_pdfs_(request, model, pk):
    clss = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', []]
    if model == '0':
        these = CNAME.objects.filter(session__exact=session.profile.session, Class__exact=clss[int(pk)]).order_by('gender', 'full_name')
        for this in these:
            this = QSUBJECT.objects.filter(student_name_id__exact=this.id, tutor__term__exact='1st Term', tutor__session__exact=session.profile.session, tutor__Class__exact=this.Class).order_by('tutor__subject')
            params, term, filename = param_cards(request, this, '0')
            pdf = Render.render('result/card.html', params, 'pdf/cards /'+pk+'/'+term[-1].split(' ')[0]+'/'+str(this.first().student_name.last_name)+'_'+str(this.first().student_name.first_name)+'.zip', filename)
            clss[-1].append((filename + ".pdf", pdf))
    else:
        tutors = BTUTOR.objects.filter(Class__exact=clss[int(pk)])
        for tutor in tutors:
            params, filepath, filename = param_marksheets(request, tutor, myHod)
            pdf =  Render.render('result/MarkSheetPdf.html', params, filepath+'.zip', filename)
            clss[-1].append((filename + ".pdf", pdf))
    return clss

