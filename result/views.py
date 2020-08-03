from .models import QSUBJECT, Edit_User, BTUTOR, CNAME,  TUTOR_HOME, ASUBJECTS, QUESTION, STUDENT
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
start_time =  time.time()
from .utils import session, Render, do_positions
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
    return render(request, 'result/desktops.html',{'pk':1, 'names':[i for i in range(100)], 'jss1':mains[0], 'jss2':mains[1], 'jss3':mains[2], 'sss1':mains[3], 'sss2':mains[4], 'sss3':mains[5], 'qry':BTUTOR.objects.filter(pk=pk).first()})

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
        page = TUTOR_HOME.objects.filter(tutor=request.user, first_term__session__exact=session.profile.session).order_by('id')
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
    if request.GET.get('student_id', False) != False:
        id = request.GET.get('student_id')
        if id:
            query = STUDENT.objects.filter(student_id__exact=id)
            this_student = QSUBJECT.objects.filter(student_id = id).first()
            if query.count() == 0:
                query = QSUBJECT.objects.filter(student_id__exact=id, tutor__term__exact='1st Term')
                if query.count() != 0:
                    [STUDENT(first=i).save() for i in query]
                    data = {'redirect':'detail/'+str(this_student.id)}
                else:
                    data = {'redirect':'logins'}
                return JsonResponse(data)
        else:
            data = {'redirect':'logins'} 
            return JsonResponse(data)
    else:
        return render(request, 'registration/log_in.html')

def detail(request, pk):
    this_student = QSUBJECT.objects.get(pk = pk)
    query = STUDENT.objects.filter(student_id__exact=this_student.student_id)
    return render(request, 'result/student_log.html',  {'query': query, 'name': this_student.student_name, 'class':this_student.tutor.Class})
            #
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
    tutor.save()
    from .utils import do_positions
    th = [i[0] for i in list(QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id').values_list('posi'))]
    if 'th' in th:
        posi = do_positions([i.avr for i in QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id') if i != 'None'])
        [save(posi[i], QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')[i].id) for i in range(0, len(posi))]
    term = ['-', '1st Term', '2nd Term', '3rd Term'][sorted([int(i) for i in [tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]]])[-1]]
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('gender', 'student_name')
    if mains.count() != 0 and md == '1':
        if request.user.is_authenticated:#pk to download results pdf
            user = Edit_User.objects.get(user = request.user)
            user.account_id = tutor.id
            user.save()
        return render(request, 'result/margged.html',  {'urs':mains.count(), 'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains), 'subject_scores':round(mains.aggregate(Sum('avr'))['avr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('avr'))['avr__avg'],2), 'qry' : tutor, 'pk': pk, 'term':term, 'classNames':CNAME.objects.filter(Class__exact=tutor.Class).order_by('gender', 'full_name')})
    else:
        return redirect('home')
    
def all_View(request, pk, md):##Step 2::  every tutor home detail views all_search_lists 
    tutor = get_object_or_404(BTUTOR, pk=pk)
    mains = QSUBJECT.objects.filter(tutor__exact=tutor)#.order_by('gender')#request.user 
    if mains.count() != 0 and int(md) == 2:
        return render(request, 'result/margged.html',  {'males' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=tutor, student_name__gender__exact = 2).count(), 'all_page': mains, 'subject_scores':round(mains.aggregate(Sum('avr'))['avr__sum'], 1), 'subject_pert':round(mains.aggregate(Avg('avr'))['avr__avg'],2), 'qry' : tutor, 'pk': pk})
    else:
        return redirect('home')
    if mains.count() == 0 and md == '1':
        return redirect('upload_txt', pk=tutor.id)
#########################################################################################################################


def Student_names_list(request, pk):##Step 2::  every tutor home detail views
    gender = CNAME.objects.all().exclude(gender__exact= pk).order_by('Class', 'full_name')  
    counted = [gender.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, gender), 'counts': gender.count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})


##########################PORTAL MANAGEMENT#################################### 
def teacher_accounts(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/transfers.html', {'all_page': paginator(request, tutors), 'counts':tutors.count()})

def all_teachers(request):
    tutors = TUTOR_HOME.objects.all().order_by('teacher_name')
    return render(request, 'result/all_transfers.html', {'tutors': tutors, 'counts':tutors.count()})

def results_junior_senior(request, pk):
    cls = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']
    tutors = BTUTOR.objects.filter(Class__exact=cls[int(pk)]).exclude(accounts__exact=None).order_by('term')
    return render(request, 'result/results_junior_senior.html', {'all_page': paginator(request, tutors), 'pk':pk, 'counts':tutors.count()})

def all_users(request):#show single candidate profile 
    qry = User.objects.all()
    return render(request, 'result/all_users.html', {'qry' : qry})

def student_subject_detail_one_subject(request, pk):#################################
    this = QSUBJECT.objects.filter(student_name_id__exact=pk).first()
    if this:
        term = [int(i) for i in [this.tutor.first_term[0], this.tutor.second_term[0], this.tutor.third_term[0]]]
        term = ['-', '1st Term', '2nd Term', '3rd Term'][sorted(term)[-1]]
        subjects = QSUBJECT.objects.filter(student_name__exact = this.student_name, tutor__Class__exact=this.tutor.Class, tutor__term__exact='1st Term', tutor__session__exact=this.tutor.session)
        lists = [x for x in subjects]
        if len(lists) != 10:
            lists = lists + [None]*(10-len(lists))
        a,b,c,d,e,f,g,h,i,j = lists
        return render(request, 'result/three_termx.html',  {'term':term, 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,'j': j, 'margged':QSUBJECT.objects.filter(tutor__subject__name__exact="ENG", tutor__Class__exact=this.tutor.Class, tutor__term__exact='1st Term', tutor__session__exact=this.tutor.session), 'this':this, 'info':this.student_name})
    else:
        return redirect('student_info', pk=pk)
def student_info (request, pk):
    query = QSUBJECT.objects.filter(tutor__Class__exact=CNAME.objects.get(pk=pk).Class)
    if CNAME.objects.get(pk=pk).birth_date:
             birth = "{:%Y-%m-%d}".format(CNAME.objects.get(pk=pk).birth_date)
    else:
          birth = '2011-02-23'
    return render(request, 'result/student_info.html',  {'info':CNAME.objects.get(pk=pk), 'birth_date':birth, 'current':CNAME.objects.filter(full_name__in=[i.student_name.full_name for i in query if i.student_name is not None]), 'pk':pk})    

def student_info_json (request):
        names = ["name", "class", "term", "opened", "presence", "punctual", "comment", "hbegin", "hend", "wbegin", "wend", "daysAbsent", "purpose", "good", "fair", "poor", "remark", "event", "indoor", "ball", "combat", "track", "jump", "throw", "swim", "lift", "sport_comment", "club_one", "office_one", "contrib_one", "club_two", "office_two", "contrib_two", 'birth', 'title','pname','pocp','contact1','contact2','address']
        listed = [request.GET.get(i) for i in names]
        info = CNAME.objects.get(pk = request.GET.get('pk'))
        info.full_name, info.Class, info.term, info.no_open, info.no_present, info.no_absent, info.comment, info.H_begin, info.H_end,info.W_begin, info.W_end, info.no_of_day_abs, info.purpose, info.good, info.fair, info.poor,info.remark, info.event, info.indoor, info.ball, info.combat, info.track, info.jump, info.throw, info.swim, info.lift, info.sport_comment, info.club_one, info.office_one, info.contrib_one, info.club_two, info.office_two, info.contrib_two, info.birth_date, info.title, info.p_name,info.occupation, info.contact1, info.contact2, info.address = listed
        info.save()
        data = {'status': "Saved!"}
        return JsonResponse(data)

def card_comment(request):
    obj = get_object_or_404(CNAME, pk=request.GET.get('uid'))
    masters = User.objects.filter(groups__name='Master')
    principals = User.objects.filter(groups__name='Principal')
    if request.user in masters:
        obj.master_comment = request.GET.get('master_comment')
        obj.save()
        data = {'status': "master"}
    elif request.user in principals:
        obj.master_comment = request.GET.get('master_comment')
        obj.principal_comment = request.GET.get('principal_comment')
        obj.save()
        data = {'status': "principal"}
    else:
        data = {'status': "None"}
    return JsonResponse(data)

def searchs(request):
    query = request.GET.get("q")
    reg = CNAME.objects.filter(last_name__icontains = query.upper()).order_by('Class', 'full_name')  
    counted = [CNAME.objects.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, reg), 'counts': CNAME.objects.all().count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})
    	

def search_results(request, pk):
        redir = [x[0] for x in list(QSUBJECT.objects.filter(student_id=CNAME.objects.get(pk=pk).student_id).values_list('id'))]
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
    this_student = CNAME.objects.filter(id__exact = id[0]).first()
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
    def get(self, request, ty, sx):
        from django.utils import timezone
        if ty == '1':
            many = get_object_or_404(QSUBJECT, pk = sx)
            term = [int(i) for i in [many.tutor.first_term[0], many.tutor.second_term[0], many.tutor.third_term[0]]]
            filename = many.tutor.subject.name+"_"+many.tutor.Class+'_'+str(term[-1])+'_'+many.student_name.full_name+'_'+many.tutor.session[-2:]
            path = os.path.join(settings.MEDIA_ROOT, 'pdf/cards/'+filename)
            info = CNAME.objects.filter(student_id__exact=many.student_id, Class__exact=many.tutor.Class, term__exact=many.tutor.term, session__exact=session).first()
            subjects = QSUBJECT.objects.filter(student_name__exact = many.student_name, tutor__Class__exact=many.tutor.Class, tutor__term__exact=many.tutor.term, tutor__session__exact=session)
            lists = [x for x in subjects]
            if len(lists) != 11:
                lists = lists + [None]*(11-len(lists))
            params = {
                'a' : lists[0], 'b':lists[1], 'c':lists[2], 'd':lists[3], 'e':lists[4], 'f' : lists[5], 'g':lists[6], 'h':lists[7], 'i':lists[8], 'j':lists[9], 'k':lists[10], 'this':many, 'today': timezone.now(), 'request': request, 'info':info
            }
            return Render.render('result/card.html', params, filename)
        
        hods = User.objects.filter(groups__name__exact='Heads')
        myHod = hods.filter(profile__department__exact=request.user.profile.department)
        if ty == '2':
            tutor = get_object_or_404(BTUTOR, pk = int(request.user.profile.account_id))
            term = [int(i) for i in [tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]]]
            filename = tutor.subject.name+"_"+tutor.Class+'_'+str(sorted(term)[-1])+'_'+tutor.session[-2:]+'_'+str(sx)
            latest = ['-', '1st Term', '2nd Term', '3rd Term'][sorted(term)[-1]]
            subjects = QSUBJECT.objects.filter(tutor__exact=tutor).exclude(student_name__gender=sx).order_by('gender', 'student_name')
            if subjects:
                sumed = round(subjects.aggregate(Sum('avr'))['avr__sum'], 1)
                average = round(subjects.aggregate(Avg('avr'))['avr__avg'], 2)
                params = {
                'subjects' : subjects, 'qry':tutor,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average, 'term':latest, 'myHod':myHod.first()
                  }
                return Render.render('result/forPdf.html', params, filename)
            else:
                return redirect('home')
        if ty == '3':
            if request.user.profile.class_in:
                SSS = [['CHE', 'ACC', 'ARB'], ['GOV', 'ICT'], ['GEO', 'AGR', 'YOR'], ['BIO', 'ECO'], ['PHY', 'LIT', 'COM'], ['ELE', 'CTR', 'GRM'], ['MAT'], ['IRS'], ['CIV'], ['ENG']]
                JSS = [['YOR'], ['BST'], ['ARB'], ['HIS'], ['PRV'], ['MAT'], ['NAV'], ['BUS'], ['IRS'], ['ENG']]
                eng = QSUBJECT.objects.filter(tutor__subject__name__exact='ENG', tutor__Class__exact=request.user.profile.class_in, tutor__session__exact=session.profile.session).order_by('gender', 'student_name')
                if eng:
                    ai, bn, cs, dd, ed, fc, gv, hs, iw, jd  = [QSUBJECT.objects.filter(student_name__in=[i.student_name for i in eng], tutor__Class__exact=request.user.profile.class_in, tutor__session__exact=eng.first().tutor.session, tutor__subject__name__in=i).order_by('gender', 'student_name') for i in [SSS, JSS][['SSS', 'JSS'].index(request.user.profile.class_in[:3])]]
                    [i.save() for i in ai]
                    posi = do_positions([int(i.annual_avr) for i in ai if i.annual_avr != 'None'])
                    sub = [["CHE, ACC, ARB", "GOV, ICT", "GEO, AGR, YOR", "BIO, ECO", "PHY, LIT, COM", "ELE, CTR, GRM", 'MAT', 'IRS', 'CIV', 'ENG'], ['YOR', 'BST', 'ARB', 'HIS', 'PRV', 'MAT', 'NAV', 'BUS', 'IRS', 'ENG']]
                    sumed = round(ai.aggregate(Sum('annual_avr'))['annual_avr__sum'], 1)
                    average = round(ai.aggregate(Avg('annual_avr'))['annual_avr__avg'], 2)
                    params = {
                        'subjects':zip(ai, bn, cs, dd, ed, fc, gv, hs, iw, jd, posi), 'Class':request.user.profile.class_in,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average, 'term':'BROADSHEET', 'subs':sub[['SSS', 'JSS'].index(request.user.profile.class_in[:3])], 'myHod':myHod.first(), 'males':eng.filter(gender__exact=1).count(), 'females':eng.filter(gender__exact=2).count()
                        }
                    return Render.render('result/broadsheet.html', params, request.user.profile.class_in)
                else:
                    return redirect('home')
            else:
                return redirect('home')

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
def name_down(request, pk, fm,  ps):
    if fm == '2':
       return redirect('pdf', ty=3, sx=0)
    pair_subject =  ['', 'CHE', 'ACC', 'ARB', 'GOV', 'ICT', 'GEO', 'AGR', 'YOR', 'BIO', 'ECO', 'PHY', 'LIT', 'COM', 'ELE', 'CTR', 'GRM']
    Class = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', ''][int(pk)]
    response = HttpResponse(content_type=[' ', 'application/csv', 'application/pdf', 'text/plain'][int(fm)])
    contents = QSUBJECT.objects.filter(tutor__Class__exact=Class, tutor__subject__name__exact=pair_subject[int(ps)], tutor__session__exact=session.profile.session).order_by('gender', 'student_name')
    if pk == '6':
        contents = QSUBJECT.objects.filter(tutor__exact=BTUTOR.objects.get(pk=int(request.user.profile.account_id))).order_by('gender', 'student_name')
        sd = [[x.student_name.full_name, x.test, x.agn, x.atd, x.total, x.exam, x.agr, x.sagr, x.fagr, x.aagr, x.avr, x.grade, x.posi] for x in contents]
        sd = [['Student Name', 'Test', 'Agn', 'Atd', 'Total', 'Exam', '3rd', '2nd', '1st', 'Anuual', 'Avg', 'Grade', 'Posi']]+sd
        Class = BTUTOR.objects.get(pk=int(request.user.profile.account_id)).Class
    elif len(contents) == 0:
        contents = CNAME.objects.filter(Class__exact=Class, session__exact=session.profile.session).order_by('gender', 'full_name')
        sd = [[x.id, x.full_name, 0, 0, 0, 0] for x in contents]
    else:
        sd = [[x.student_name.id, x.student_name.full_name, 0, 0, 0, 0] for x in contents]
        Class = Class +'_'+pair_subject[int(ps)]
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] = "attachment; filename={name}".format(name=Class+[' ', '.csv', '.pdf', '.txt'][int(fm)])
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
