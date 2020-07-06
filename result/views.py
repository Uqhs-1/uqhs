from .models import QSUBJECT, Edit_User, ANNUAL, BTUTOR, CNAME, OVERALL_ANNUAL, TUTOR_HOME, REGISTERED_ID, ASUBJECTS, QUESTION, STUDENT, STUDENT_INFO
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
from django.contrib.auth.decorators import login_required
from datetime import timedelta 
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg
from django.http import JsonResponse
from django.views.generic import View
from django.conf import settings
import os, requests

#########################################################################################################################
start_time = time.time()
from .utils import session, Render
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

def offline(request, pk):
    mains = [BTUTOR.objects.filter(Class__exact=i).order_by('id') for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/desktops.html',{'pk':1, 'names':[i for i in range(100)], 'jss1':mains[0], 'jss2':mains[1], 'jss3':mains[2], 'sss1':mains[3], 'sss2':mains[4], 'sss3':mains[5]})

def mobiles(request, pk):
    mains = [BTUTOR.objects.filter(Class__exact=i).order_by('id') for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/mobiles.html',{'pk':1, 'names':[i for i in range(100)], 'jss1':mains[0], 'jss2':mains[1], 'jss3':mains[2], 'sss1':mains[3], 'sss2':mains[4], 'sss3':mains[5]})

def uniqueness(request, pk): 
    tutor = BTUTOR.objects.get(pk=pk) 
    unique = TUTOR_HOME.objects.filter(first_term__accounts__exact=tutor.accounts, first_term__session__exact = tutor.session)
    return render(request, 'result/page.html', {'page':unique})


def home(request):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every tutor!
    """
    # If a tutor is authenticated then redirect them to the tutor's page
    if request.user.is_authenticated:#a tutor page 
        page = TUTOR_HOME.objects.filter(tutor=request.user, first_term__session__exact=session).order_by('id')
        import datetime
        present = datetime.datetime.today()
        past = request.user.last_login
        if present.year != past.year or present.month != past.month or present.day != past.day:
            login_count = request.user.profile.login_count
            login_count += 1
            user = Edit_User.objects.get(user=request.user)
            user.login_count = login_count
            user.save()
        return render(request, 'result/page.html', {'page':page})
    else:#general login page
        return redirect('logins')

def student_home_page(request):
    if request.method == 'POST':
        id = request.POST.get('studentid', False)
        if id != False:
            query = STUDENT.objects.filter(student_id__exact=id)
            this_student = REGISTERED_ID.objects.filter(id = id.split('/')[-1]).first()
            if query.count() == 0:
                query = QSUBJECT.objects.filter(student_id__exact=id, tutor__term__exact='1st Term')
                if query.count() != 0:
                    [STUDENT(first=i).save() for i in query]
                else:
                    return redirect('logins')
                query = STUDENT.objects.filter(student_id__exact=id)
            return render(request, 'result/student_log.html',  {'query': query, 'name': query[0].student_name, 'class':this_student.student_class})
            #
        else:
            return redirect('logins') 
    else:
        return render(request, 'registration/log_in.html')
       
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


def subject_home(request, pk, cl):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every subject!
    """
    tutor = BTUTOR.objects.get(pk=pk)
    if cl == '1':#class
        detail = 'Results filtered by Class'
        tutor = BTUTOR.objects.filter(Class__exact=tutor.Class).order_by('session')
    elif cl == '2':#term
        detail = 'Results filtered by Term'
        tutor = BTUTOR.objects.filter(term__exact=tutor.term).order_by('session')
    elif cl == '3':#subject
        detail = 'Results filtered by Subject'
        tutor = BTUTOR.objects.filter(subject__exact=tutor.subject).order_by('session', 'Class')
    if tutor.count() != 0:    
        return render(request, 'result/tutor_class_filter.html', {'tutors':tutor, 'detail' : detail, 'counts':tutor.count()})
    else:
        return redirect('home') 
def save(posi, pk):
    obj = get_object_or_404(QSUBJECT, pk=pk)
    obj.posi = posi
    obj.save()

def detailView(request, pk, md):##Step 2::  every tutor home detail views all_search_lists
    tutor = get_object_or_404(BTUTOR, pk=pk)
    from .utils import do_positions
    th = [i[0] for i in list(QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id').values_list('posi'))]
    if 'th' in th:
        posi = do_positions([int(i.agr) for i in QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')])
        [save(posi[i], QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')[i].id) for i in range(0, len(posi))]
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')
    if mains.count() != 0 and md == '1':
        return render(request, 'result/margged.html',  {'urs':mains.count(), 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains), 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk, 'classNames':REGISTERED_ID.objects.filter(student_class__exact=tutor.Class, session__exact=tutor.session)})
    else:
        return redirect('home')
    
def all_View(request, pk, md):##Step 2::  every tutor home detail views all_search_lists 
    tutor = get_object_or_404(BTUTOR, pk=pk)
    mains = QSUBJECT.objects.filter(tutor__exact=tutor)#.order_by('gender')#request.user 
    if mains.count() != 0 and int(md) == 2:
        return render(request, 'result/margged.html',  {'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk})
    else:
        return redirect('home')
    if mains.count() == 0 and md == '1':
        return redirect('upload_txt', pk=tutor.id)
#########################################################################################################################
@login_required   
def genders_scores(request, pk_code):##Step 2::  every tutor home detail views all_search_lists
    gender = [['a', 'b'], [1, 2]]
    tutor = get_object_or_404(BTUTOR, pk=pk_code[:-1])
    pro = get_object_or_404(Edit_User, user=request.user)
    pro.account_id = str(pk_code[:-1])+'_'+str(gender[1][gender[0].index(pk_code[-1])])
    mains = QSUBJECT.objects.filter(tutor__exact=tutor, gender = gender[1][gender[0].index(pk_code[-1])]).order_by('student_name')#request.user 
    if mains.count() != 0:
        return render(request, 'result/margged.html',  {'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('agr'))['agr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('agr'))['agr__avg'],2), 'qry' : tutor, 'pk': pk_code[:-1]})
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
def student_subject_list(request, pk):##Step 2::  every tutor home detail views  student_subject_list
    mains = QSUBJECT.objects.filter(student_id=QSUBJECT.objects.get(pk=pk).student_id, tutor__session__exact=session).order_by('id')
    return render(request, 'result/student_subject_list.html',  {'all_page': paginator(request, mains), 'counts': mains.count(), 'name': QSUBJECT.objects.get(pk=pk).student_name, 'pk': pk})

def all_student_subject_list(request, pk):##Step 2::  every tutor home detail views
    mains = QSUBJECT.objects.filter(student_id=QSUBJECT.objects.get(pk=pk).student_id, tutor__session__exact=session)
    return render(request, 'result/all_student_subject_list.html',  {'mains': mains, 'counts': mains.count(), 'name': QSUBJECT.objects.get(pk=pk), 'pk': pk, 'cnt': pk})
##########################PORTAL MANAGEMENT#################################### 
def teacher_accounts(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/transfers.html', {'all_page': paginator(request, tutors), 'counts':tutors.count()})

def all_teachers(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/all_transfers.html', {'tutors': tutors, 'counts':tutors.count()})

def home_page_return(request, pk):
    tutor = tutor
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

def student_subject_detail_one_subject(request, pk):#################################
    many = get_object_or_404(QSUBJECT, pk=pk)
    if many.tutor.term == '1st Term' or many.tutor.term == '2nd Term':
        subjects = QSUBJECT.objects.filter(student_name__exact = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact=many.tutor.term, tutor__session__exact=session)
    else:
        subjects = ANNUAL.objects.filter(student_name__exact = many.student_name, subject_by__Class__exact=many.tutor.Class, subject_by__term__exact=many.tutor.term, subject_by__session__exact=session)
    lists = [x for x in subjects]
    
    if len(lists) != 11:
        lists = lists + [None]*(11-len(lists))
    if subjects.count() != 0:
        info = STUDENT_INFO.objects.filter(student_id__exact=many.student_id, Class__exact=many.tutor.Class, term__exact=many.tutor.term, session__exact=session).first()
        if many.tutor.term == '1st Term' or many.tutor.term == '2nd Term':
            return render(request, 'result/single_term.html',  {'a' : lists[0], 'b':lists[1], 'c':lists[2], 'd':lists[3], 'e':lists[4], 'f' : lists[5], 'g':lists[6], 'h':lists[7], 'i':lists[8], 'j':lists[9], 'k':lists[10], 'info':info,'margged':QSUBJECT.objects.filter(tutor__subject__name__exact="ENG", tutor__Class__exact=many.tutor.Class, tutor__term__exact=many.tutor.term, tutor__session__exact=session), 'this':many}) 
        else:
            first = QSUBJECT.objects.filter(student_name = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact='1st Term', tutor__session__exact=session)
            second = QSUBJECT.objects.filter(student_name = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact='2nd Term', tutor__session__exact=session)
            mpr = ANNUAL.objects.filter(student_name__exact = many.student_name, subject_by__Class__exact=many.tutor.Class, subject_by__term__exact=many.tutor.term, subject_by__subject__exact=many.tutor.subject, subject_by__session__exact=session).first()
            annual = ANNUAL.objects.filter(subject_by__subject__name__exact="ENG", subject_by__Class__exact=many.tutor.Class, subject_by__term__exact=many.tutor.term, subject_by__session__exact=session)
            return render(request, 'result/three_termx.html',  {'a' : lists[0], 'b':lists[1], 'c':lists[2], 'd':lists[3], 'e':lists[4], 'f' : lists[5], 'g':lists[6], 'h':lists[7], 'i':lists[8], 'j':lists[9], 'k':lists[10], 'info':info, 'annual':annual, 'this':many}) 
    else:
        return redirect('home')

def card_comment(request):
    many = get_object_or_404(QSUBJECT, pk=request.GET.get('student_id'))
    qs = QSUBJECT.objects.filter(student_name = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact=many.tutor.term, tutor__session__exact=session)
    masters = User.objects.filter(groups__name='Master')
    principals = User.objects.filter(groups__name='Principal')
    if request.user in masters:
        for i in range(qs.count()):
            obj = qs[i]
            obj.master_comment = request.GET.get('master_comment')
            obj.save()
        data = {'status': "master"}
        return JsonResponse(data)
    elif request.user in principals:
        for i in range(qs.count()):
            obj = qs[i]
            obj.master_comment = request.GET.get('master_comment')
            obj.principal_comment = request.GET.get('principal_comment')
            obj.save()
            print("saved!")
        data = {'status': "principal"}
        return JsonResponse(data)
    else:
        data = {'status': "None"}
        return JsonResponse(data)

def searchs(request):
    query = request.GET.get("q")
    reg = REGISTERED_ID.objects.filter(student_name__in=CNAME.objects.filter(last_name__icontains = query.upper()), session__exact=session)
    return render(request, 'result/searched_names.html',  {'all_page' : reg}) 	

def search_results(request, pk):
        redir = [x[0] for x in list(QSUBJECT.objects.filter(student_id=REGISTERED_ID.objects.get(pk=pk).student_id).values_list('id'))]
        return redirect('student_subject_list', pk=redir[0])
    
    
def quest_filter(request, tm, cl, sj):
    quetions = QUESTION.objects.filter(subjects__exact=sj,classes__exact=QSUBJECT.objects.get(pk=int(cl)).tutor.Class,terms__exact=['1st Term', '2nd Term', '3rd Term', None][int(tm)])
    return render(request, 'result/quetions.html', {'quetions':quetions, 'Subject':sj, 'Class':QSUBJECT.objects.get(pk=int(cl)).tutor.Class, 'Term':['1st Term', '2nd Term', '3rd Term', None][int(tm)]})
@login_required 
def editQuest(request, pk):
    if request.GET.get('question', None) != None:
        question = QUESTION.objects.get(pk=int(request.GET.get('pk')))
        question.question=request.GET.get('question')
        question.optionA=request.GET.get('optionA')
        question.optionB=request.GET.get('optionB')
        question.optionC=request.GET.get('optionC')
        question.optionD=request.GET.get('optionD')
        question.answerA=request.GET.get('answerA')
        question.answerB=request.GET.get('answerB')
        question.answerC=request.GET.get('answerC')
        question.answerD=request.GET.get('answerD')
        question.comment=request.GET.get('AnswerComment')
        question.CORRECT=request.GET.get('correctAnswer')
        question.save()
        data = {'status': "Saved!"}
        return JsonResponse(data)
    else:
        quetions = QUESTION.objects.get(pk=pk)
        return render(request, 'result/question_model.html', {'scr':quetions})


    

def student_exam_page(request, pk, SUB):
    id = [pk, str(SUB)]
    this_student = REGISTERED_ID.objects.filter(id__exact = id[0]).first()
    if this_student != None:
        query = QSUBJECT.objects.filter(student_id__exact = this_student, tutor__subject__name__exact=id[1], tutor__term__exact='1st Term', tutor__Class__exact=this_student.student_class, tutor__session__exact=session)
        if query.count() == 1:#1st term exist
            tm = '2nd Term'
            quetions = QUESTION.objects.filter(subjects__exact=id[1],classes__exact=this_student.student_class,terms__exact='2nd Term', session__exact=session)
        query = QSUBJECT.objects.filter(student_id__exact = this_student, tutor__subject__name__exact=id[1], tutor__term__exact='2nd Term', tutor__Class__exact=this_student.student_class, tutor__session__exact=session)
        if query.count() == 1:#2nd term exist
            tm = '3rd Term'
            quetions = QUESTION.objects.filter(subjects__exact=id[1],classes__exact=this_student.student_class,terms__exact='3rd Term', session__exact=session)
        else:
            tm = '1st Term'#New term
            quetions = QUESTION.objects.filter(subjects__exact=id[1],classes__exact=this_student.student_class,terms__exact='1st Term', session__exact=session)
        return render(request, 'result/quetions.html', {'quetions':quetions, 'Subject':SUB, 'Class':this_student.student_class, 'Term':tm})
        	       
    else:
        return redirect('home')
from django.contrib.auth.mixins import LoginRequiredMixin 
class Pdf(LoginRequiredMixin, View):
    def get(self, request, pk, ty, sx):
        from django.utils import timezone
        if ty == '1':
            many = get_object_or_404(QSUBJECT, pk = pk)
            term = [int(i) for i in [many.tutor.first_term[0], many.tutor.second_term[0], many.tutor.third_term[0]]]
            filename = many.tutor.subject.name+"_"+many.tutor.Class+'_'+str(term[-1])+'_'+many.student_name.full_name+'_'+many.tutor.session[-2:]
            path = os.path.join(settings.MEDIA_ROOT, 'pdf/cards/'+filename)
            info = STUDENT_INFO.objects.filter(student_id__exact=many.student_id, Class__exact=many.tutor.Class, term__exact=many.tutor.term, session__exact=session).first()
            subjects = QSUBJECT.objects.filter(student_name__exact = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact=many.tutor.term, tutor__session__exact=session)
            lists = [x for x in subjects]
            if len(lists) != 11:
                lists = lists + [None]*(11-len(lists))
            params = {
                'a' : lists[0], 'b':lists[1], 'c':lists[2], 'd':lists[3], 'e':lists[4], 'f' : lists[5], 'g':lists[6], 'h':lists[7], 'i':lists[8], 'j':lists[9], 'k':lists[10], 'this':many, 'today': timezone.now(), 'request': request, 'info':info
            }
            return Render.render('result/card.html', params, path)
        if ty == '2':
            tutor = get_object_or_404(BTUTOR, pk = pk)
            term = [int(i) for i in [tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]]]
            filename = tutor.subject.name+"_"+tutor.Class+'_'+str(term[-1])+'_'+tutor.session[-2:]+'_'+str(sx)
            path = os.path.join(settings.MEDIA_ROOT, 'pdf/marksheets/'+filename)
            subjects = QSUBJECT.objects.filter(tutor__exact=tutor).exclude(student_name__gender=sx)
            sumed = round(subjects.aggregate(Sum('agr'))['agr__sum'], 1)
            average = round(subjects.aggregate(Avg('agr'))['agr__avg'], 2)
            params = {
                'subjects' : subjects, 'qry':tutor,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average
            }
            return Render.render('result/forPdf.html', params, path)
    
def do_a_write(request, pk):
    url = 'http://127.0.0.1:8838/result/render/pdf/'+str(pk)+'/'
    r = requests.get(url)
    path = os.path.join(settings.MEDIA_ROOT, 'upload/'+'/'+QSUBJECT.objects.get(pk=pk).tutor.Class+'/'+QSUBJECT.objects.get(pk=pk).tutor.term+'/'+QSUBJECT.objects.get(pk=pk).student_name.last_name+'_'+QSUBJECT.objects.get(pk=pk).student_name.first_name+'.pdf')
    with open(path, 'wb') as f:
        f.write(r.content) 
    f.close()
    data = {'status': QSUBJECT.objects.get(pk=pk).student_name.last_name+'_'+QSUBJECT.objects.get(pk=pk).student_name.first_name+' ReportCard generated.'}
    return JsonResponse(data)
@login_required 
def call_url(request, pk):
    if request.user.profile.class_in:
        listed = QSUBJECT.objects.filter(tutor__Class__exact=QSUBJECT.objects.get(pk=pk).tutor.Class, tutor__session__exact=QSUBJECT.objects.get(pk=pk).tutor.session, tutor__term__exact=QSUBJECT.objects.get(pk=pk).tutor.term, tutor__subject__name__exact='ENG')
        ids = [i[0] for i in list(listed.values_list('id'))]
        [do_a_write(request, i) for i in ids]
    return redirect('pdf_compressor', pk=pk)

def student_info (request, pk):
    if int(pk) in [i[0] for i in list(STUDENT_INFO.objects.all().values_list('id'))]:
        info = STUDENT_INFO.objects.get(pk = pk)
        pk = QSUBJECT.objects.filter(info_id=pk).first().id
    else:
        if STUDENT_INFO.objects.filter(student_name__exact=QSUBJECT.objects.get(pk=pk).student_name, Class__exact=QSUBJECT.objects.get(pk=pk).tutor.Class, session__exact=QSUBJECT.objects.get(pk=pk).tutor.session, term__exact=QSUBJECT.objects.get(pk=pk).tutor.term).exists():
            info = STUDENT_INFO.objects.get(student_name=QSUBJECT.objects.get(pk=pk).student_name, Class=QSUBJECT.objects.get(pk=pk).tutor.Class, session=QSUBJECT.objects.get(pk=pk).tutor.session, term=QSUBJECT.objects.get(pk=pk).tutor.term)
        else:
            info = STUDENT_INFO(student_name=QSUBJECT.objects.get(pk=pk).student_name, student_id=QSUBJECT.objects.get(pk=pk).student_id,Class=QSUBJECT.objects.get(pk=pk).tutor.Class, session=QSUBJECT.objects.get(pk=pk).tutor.session, term=QSUBJECT.objects.get(pk=pk).tutor.term)
            info.save()
            qs = QSUBJECT.objects.get(pk=pk)
            qs.info = info
            qs.save()
    return render(request, 'result/student_info.html',  {'info':info, 'current':STUDENT_INFO.objects.filter(Class=info.Class, term=info.term, session=info.session), 'pk':pk})

def student_info_json (request):
        names = ["class", "term", "opened", "presence", "punctual", "comment", "hbegin", "hend", "wbegin", "wend", "daysAbsent", "purpose", "good", "fair", "poor", "remark", "event", "indoor", "ball", "combat", "track", "jump", "throw", "swim", "lift", "sport_comment", "club_one", "office_one", "contrib_one", "club_two", "office_two", "contrib_two"]
        listed = [request.GET.get(i) for i in names]
        info = STUDENT_INFO.objects.get(pk = request.GET.get('pk'))
        info.Class, info.term, info.no_open, info.no_present, info.no_absent, info.comment, info.H_begin, info.H_end, info.W_begin, info.W_end, info.no_of_day_abs, info.purpose, info.good, info.fair, info.poor,info.remark, info.event, info.indoor, info.ball, info.combat, info.track, info.jump, info.throw, info.swim, info.lift, info.sport_comment, info.club_one, info.office_one, info.contrib_one, info.club_two, info.office_two, info.contrib_two = listed
        info.save()
        data = {'status': "Saved!"}
        return JsonResponse(data)

import csv
from django.http import HttpResponse
import zipfile
from io import BytesIO
module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'JSS 2.txt')
def sample_disply(request):
    #os.chdir(file_path)
    empty_list = open(file_path, "r" )
    return HttpResponse(empty_list, content_type='text/plain')

def sample_down(request):
    response = HttpResponse(content_type='text/plain')
    with open(file_path, 'r') as file:
        file_txt = file.read()
        contents = file_txt.split('\n');
        sd = [[x] for x in contents]
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] ='attachment; filename="samples.txt"'
    return response 
@login_required
def pdf_compressor(request, pk):
    path = os.path.join(settings.MEDIA_ROOT, 'upload/'+'/'+QSUBJECT.objects.get(
    pk=pk).tutor.Class+'/'+QSUBJECT.objects.get(pk=pk).tutor.term+'/'+QSUBJECT.objects
    .get(pk=pk).student_name.last_name+'_'+QSUBJECT.objects.get(pk=pk).student_name.first_name+'.pdf')
    fdir, fname = os.path.split(path)
    file_name = []
    with os.scandir(fdir) as dit:
         for i in dit:
            file_name += [os.path.join(fdir, i.name)]
    s=BytesIO()
    with zipfile.ZipFile(s, "w") as zf:
        for fnames in file_name:
            zf.write(fnames)
    zf.close()
    response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    response['Content-Disposition'] = "attachment; filename={Class}.zip".format(Class=QSUBJECT.objects.get(
    pk=pk).tutor.Class)
    return response