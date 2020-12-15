from .models import QSUBJECT, Edit_User, BTUTOR, CNAME,  TUTOR_HOME, QUESTION
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
import csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from io import BytesIO
module_dir = os.path.dirname(__file__)  # get current directory
#########################################################################################################################
start_time =  time.time()
from random import randrange
from collections import Counter
from .utils import session, Render, Rendered, do_positions
session = session()
 

def offline(request, pk):
    if request.user.is_authenticated:
        if request.user.profile.email_confirmed:
            mains = [BTUTOR.objects.filter(Class__exact=i).order_by('id') for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
            tutor = None
            if pk != '0':
                tutor = BTUTOR.objects.get(pk=pk)
            return render(request, 'result/desktops.html',{'pk':1, 'names':[i for i in range(100)], 'jss1':mains[0], 'jss2':mains[1], 'jss3':mains[2], 'sss1':mains[3], 'sss2':mains[4], 'sss3':mains[5], 'qry':tutor})
        else:
            return redirect('home')
    else:
        return redirect('subject_view', pk=pk, md=1)

def uniqueness(request, pk): 
    tutor = BTUTOR.objects.get(pk=pk) 
    unique = TUTOR_HOME.objects.filter(first_term__accounts__exact=tutor.accounts, first_term__session__exact = tutor.session)
    return render(request, 'result/page.html', {'tutor':unique.first(), 'page':unique})


def home(request):#Step 1:: list of tutor's subjects with class, term
    """
    Home page for every tutor!
    """
    # If a tutor is authenticated then redirect them to the tutor's page
    if request.user.is_authenticated:#a tutor page 
        page = TUTOR_HOME.objects.filter(tutor=request.user).order_by('updated')#, first_term__session__exact=session.profile.session).order_by('id')
        import datetime
        present = datetime.datetime.today()
        past = request.user.last_login
        if present.year != past.year or present.month != past.month or present.day != past.day:
            login_count = request.user.profile.login_count
            login_count += 1
            user = Edit_User.objects.get(user=request.user)
            user.login_count = login_count
            user.save()
        return render(request, 'result/page.html', {'page':page, 'tutor':page.first()})
    else:#general login page
        return redirect('logins')

def student_exam_page(request, subj_code, pk):
    info = get_object_or_404(CNAME, pk=pk)
    sub_code = ["ACC", "AGR", "ARB", "BIO", "BST", "BUS", "CHE", "CIV", "COM", "CTR", "ECO", "ELE", "ENG", "FUR", "GEO", "GOV", "GRM", "HIS", "ICT", "IRS", "LIT", "MAT", "NAV", "PHY", "PRV", "YOR"]
    if request.GET.get('done', False) != False:
        qr = QSUBJECT.objects.filter(student_name_id__exact=info.id,tutor__subject__exact=sub_code[int(subj_code)], tutor__session__exact=session.profile.session)
        if qr:
        	qr.first().exam = int(request.GET.get('scores'))
        else:
        	qr = QSUBJECT(student_name=info, exam=int(request.GET.get('scores')), tutor=BTUTOR.objects.filter(Class__exact=info.Class,subject__exact=sub_code[int(subj_code)],session__exact=session.profile.session).first())
        qr.save()
        return JsonResponse({'status':str(qr.created)})

    quetions = QUESTION.objects.filter(subjects__exact=sub_code[int(subj_code)], classes__exact=info.Class, terms__exact=info.term, session__exact= session.profile.session)
    return render(request, 'result/quetions.html', {'quetions':quetions, 'Subject':sub_code[int(subj_code)], 'Class':info.Class, 'Term':info.term})


#@login_required
def student_home_page(request, pk):
    info = get_object_or_404(CNAME, pk=pk)
    if request.GET.get('pk', False) != False:
        qr = QSUBJECT.objects.get(pk=int(request.GET.get('pk', False)))
        return JsonResponse({'status':str(qr.delete())})
    query = QSUBJECT.objects.filter(student_name_id__exact=info.id, tutor__term__exact='1st Term', tutor__session__exact=session.profile.session, tutor__Class__exact=info.Class).order_by('updated')
    return render(request, 'result/student_form.html', {'info':info, 'detail':query})
       
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
def save(mod, posi, pk):
    obj = get_object_or_404(mod, pk=pk)
    obj.posi = posi
    obj.save()

def common(request, pk):
    tutor = get_object_or_404(BTUTOR, pk=pk)
    tutor.save()
    th = [i[0] for i in list(QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id').values_list('posi'))]
    if 'th' in th:
        posi = do_positions([i.avr for i in QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id') if i.avr != None])
        [save(QSUBJECT, posi[i], QSUBJECT.objects.filter(tutor__exact=tutor).order_by('id')[i].id) for i in range(0, len(posi))]
    term = ['-', '1st Term', '2nd Term', '3rd Term'][sorted([int(i) for i in [tutor.first_term[0], tutor.second_term[0], tutor.third_term[0]]])[-1]]
    mains = QSUBJECT.objects.filter(tutor__exact=tutor).order_by('gender', 'student_id')#.exclude(fagr__exact=0)
    return [term,  mains, tutor]
def detailView(request, pk, md):##Step 2::  every tutor home detail views all_search_lists
    mains = common(request, pk)
    if mains[1].count() != 0 and md == '1':
        if request.user.is_authenticated:#pk to download results pdf
            user = request.user.profile
            user.account_id = mains[2].id
            user.save()
        return render(request, 'result/margged.html',  {'urs':mains[1].count(), 'males' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 2).count(), 'all_page': paginator(request, mains[1]), 'subject_scores':round(mains[1].aggregate(Sum('avr'))['avr__sum'], 1), 'subject_pert':round(mains[1].aggregate(Avg('avr'))['avr__avg'],2), 'qry' : mains[2], 'pk': pk, 'term':mains[0], 'classNames':CNAME.objects.filter(Class__exact=mains[2].Class).order_by('gender', 'full_name')})
    else:
        return redirect('home')
    
def all_View(request, pk, md):##Step 2::  every tutor home detail views all_search_lists 
    mains = common(request, pk)#.order_by('gender')#request.user 
    if mains[1].count() != 0 and int(md) == 2:
        return render(request, 'result/margged.html',  {'males' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 1).count(), 'females' : QSUBJECT.objects.filter(tutor__exact=mains[2], student_name__gender__exact = 2).count(), 'all_page': mains[1], 'subject_scores':round(mains[1].aggregate(Sum('avr'))['avr__sum'], 1), 'subject_pert':round(mains[1].aggregate(Avg('avr'))['avr__avg'],2),  'term':mains[0], 'qry' : mains[2], 'pk': pk})
    else:
        return redirect('home')
    
#########################################################################################################################


def Student_names_list(request, pk):##Step 2::  every tutor home detail views
    gender = CNAME.objects.all().exclude(gender__exact= pk).order_by('gender', 'full_name')  
    counted = [gender.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, gender), 'counts': gender.count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})


##########################PORTAL MANAGEMENT#################################### 
def teacher_accounts(request):
    tutors = TUTOR_HOME.objects.all().order_by('tutor__username')
    return render(request, 'result/transfers.html', {'all_page': paginator(request, tutors), 'counts':tutors.count()})


def results_junior_senior(request, pk):
    cls = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']
    tutors = BTUTOR.objects.filter(Class__exact=cls[int(pk)]).exclude(accounts__exact=None).order_by('updated')
    return render(request, 'result/results_junior_senior.html', {'all_page': paginator(request, tutors), 'pk':pk, 'counts':tutors.count()})

def all_users(request):#show single candidate profile 
    qry = User.objects.all().order_by('username') 
    return render(request, 'result/all_users.html', {'qry' : qry})

def student_info (request, pk):
    query = QSUBJECT.objects.filter(tutor__Class__exact=CNAME.objects.get(pk=pk).Class).order_by('gender', 'student_name')
    if CNAME.objects.get(pk=pk).birth_date:
             birth = "{:%Y-%m-%d}".format(CNAME.objects.get(pk=pk).birth_date)
    else:
          birth = '2011-02-23'
    return render(request, 'result/student_info.html',  {'info':CNAME.objects.get(pk=pk), 'birth_date':birth, 'current':CNAME.objects.filter(Class__exact=CNAME.objects.get(pk=pk).Class), 'pk':pk})    

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
    reg = CNAME.objects.filter(last_name__icontains = query.upper()).order_by('gender', 'full_name')  
    counted = [CNAME.objects.filter(Class__exact=i).count() for i in ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    return render(request, 'result/searched_names.html',  {'all_page': paginator(request, reg), 'counts': CNAME.objects.all().count(), 'Jo': counted[0], 'Jt': counted[1], 'Jh': counted[2], 'So': counted[3], 'St': counted[4], 'Sh': counted[5]})
    	

def search_results(request, pk):
        redir = [x[0] for x in list(QSUBJECT.objects.filter(student_id=CNAME.objects.get(pk=pk).student_id).values_list('id'))]
        return redirect('student_subject_list', pk=redir[0])
        

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

def grade_counter(query):
    grade_counts = Counter([i.grade for i in query])
    ordered = grade_counts.most_common()
    return ordered
class Pdf(LoginRequiredMixin, View):
    def get(self, request, ty, sx):#CARD
        from django.utils import timezone
        if ty == '1' or ty == '4':
              this = QSUBJECT.objects.filter(student_name_id__exact=sx, tutor__term__exact='1st Term', tutor__session__exact=session.profile.session, tutor__Class__exact=CNAME.objects.get(pk=sx).Class).order_by('updated')
               
              if this:  
                 term = sorted([this.first().tutor.first_term, this.first().tutor.second_term, this.first().tutor.third_term])       
                 lists = [x for x in this][:10]
                 if len(lists) != 10:
                    lists = lists + [None]*(10-len(lists))
                 a,b,c,d,e,f,g,h,i,j = lists
                 if ty == '4':
                     return render(request, 'result/three_termx.html',  {'term':term[-1], 'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,'j': j, 'margged':CNAME.objects.filter(Class__exact=this.first().tutor.Class, session__exact=session.profile.session), 'info':this.first().student_name})
                 params = {
                     'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f, 'g': g, 'h': h, 'i': i,'j': j, 'this':this.first(), 'today': timezone.now(), 'request': request, 'term':term[-1], 'info':this.first().student_name
                          }
                 return Render.render('result/card.html', params, 'cards/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(this.first().tutor.Class))+'/'+term[-1].split(' ')[0]+'/'+str(this.first().student_name.id), str(this.first().student_name.id))
              else:
                 return redirect('student_info', pk=sx)        
        hods = User.objects.filter(groups__name__exact='Heads')
        myHod = hods.filter(profile__department__exact=request.user.profile.department)
        if ty == '2':#SCORE SHEET
            tutor = get_object_or_404(BTUTOR, pk = int(request.user.profile.account_id))
            term = sorted([tutor.first_term, tutor.second_term, tutor.third_term])
            filepath = 'marksheets/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(tutor.Class))+'/'+term[-1].split(' ')[0]+'/'+tutor.subject+"_"+tutor.session[-2:]+'_'+str(sx)
            filename = tutor.subject+"_"+tutor.session[-2:]+'_'+str(sx)
            subjects = QSUBJECT.objects.filter(tutor__exact=tutor).exclude(student_name__gender=sx).order_by('gender', 'student_id')
            if subjects:
                sumed = round(subjects.aggregate(Sum('avr'))['avr__sum'], 1)
                average = round(subjects.aggregate(Avg('avr'))['avr__avg'], 2)
                params = {
                'subjects' : subjects, 'qry':tutor,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average, 'term':term[-1], 'myHod':myHod.first(), 'grade_conuts':grade_counter(subjects)
                  }
                return Render.render('result/MarkSheetPdf.html', params, filepath, filename)
            else:
                return redirect('home')
        if ty == '3':#BROADSHEET
            if request.user.profile.class_in:
                SSS = [['CHE', 'ACC', 'ARB'], ['GOV', 'ICT'], ['GEO', 'AGR', 'YOR'], ['BIO', 'ECO'], ['PHY', 'LIT', 'COM'], ['ELE', 'CTR', 'GRM'], ['MAT'], ['IRS'], ['CIV'], ['ENG']]
                JSS = [['YOR'], ['BST'], ['ARB'], ['HIS'], ['PRV'], ['MAT'], ['NAV'], ['BUS'], ['IRS'], ['ENG']]           
                response = HttpResponse(content_type=[' ', 'application/csv', 'application/pdf', 'text/plain'][int(1)])
                eng = CNAME.objects.filter(Class__exact=request.user.profile.class_in).exclude(annual_scores__exact = 0)             
                sub = [["CHE, ACC, ARB", "GOV, ICT", "GEO, AGR, YOR", "BIO, ECO", "PHY, LIT, COM", "ELE, CTR, GRM", 'MAT', 'IRS', 'CIV', 'ENG'], ['YOR', 'BST', 'ARB', 'HIS', 'PRV', 'MAT', 'NAV', 'BUS', 'IRS', 'ENG']]
                if eng:
                    posi = do_positions([i.annual_avr for i in eng.order_by('id')])
                    [save(CNAME, i, k.id) for i, k in zip(posi, eng.order_by('id'))]
                    #return HttpResponse([posi], content_type='text/plain')
                    if sx == '1':
                        ai, bn, cs, dd, ed, fc, gv, hs, iw, jd  = [QSUBJECT.objects.filter(student_id__in=[i.uid for i in eng.order_by('gender', 'full_name')], tutor__Class__exact=request.user.profile.class_in, tutor__session__exact=session.profile.session, tutor__subject__in=x) for x in [SSS, JSS][['SSS', 'JSS'].index(request.user.profile.class_in[:3])]]
                        sd = [[r, a.student_name, a.agr, a.sagr, a.fagr, a.avr, b.agr, b.sagr,  b.fagr, b.avr, c.agr, c.sagr, c.fagr, c.avr, d.agr, d.sagr, d.fagr, d.avr, e.agr, e.sagr, e.fagr, e.avr, f.agr, f.sagr, f.fagr, f.avr, g.agr, g.sagr, g.fagr, g.avr, h.agr, g.sagr, h.fagr, h.avr, i.agr, i.sagr, i.fagr, i.avr, j.agr, j.sagr, j.fagr, j.avr, a.student_name.annual_scores, a.student_name.annual_avr, a.student_name.posi]  for r, a, b, c, d, e, f, g, h, i, j in zip([r for r in range(1, eng.count()+1)], ai, bn, cs, dd, ed, fc, gv, hs, iw, jd)]
                        sd = [[['sn',  'Student_name', 3, 2, 1, 'YOR', 3, 2, 1, 'BST', 3, 2, 1, 'ARB', 3, 2, 1, 'HIS', 3, 2, 1, 'PRV', 3, 2, 1, 'MAT', 3, 2, 1, 'NAV', 3, 2, 1, 'BUS', 3, 2, 1, 'IRS', 3, 2, 1, 'ENG', 'AGR', 'AVR', 'Posi'], ['sn', 'Student_name', 3, 2, 1, "CHE, ACC, ARB", 3, 2, 1, "GOV, ICT", 3, 2, 1, "GEO, AGR, YOR", 3, 2, 1, "BIO, ECO", 3, 2, 1, "PHY, LIT, COM", 3, 2, 1, "ELE, CTR, GRM", 3, 2, 1,  'MAT', 3, 2, 1, 'IRS', 3, 2, 1, 'CIV', 3, 2, 1, 'ENG', 'AGR', 'AVR', 'Posi']][['JSS', 'SSS'].index(request.user.profile.class_in[:3])]]+sd
                        writer = csv.writer(response)
                        for each in sd:
                            writer.writerow(each) 
                        response['Content-Disposition'] = "attachment; filename={name}".format(name=request.user.profile.class_in+[' ', '.csv', '.pdf', '.txt'][int(sx)])
                        return response
                    pag = ['', '', [SSS, JSS][['SSS', 'JSS'].index(request.user.profile.class_in[:3])][:5], [SSS, JSS][['SSS', 'JSS'].index(request.user.profile.class_in[:3])][5:]]
                    tit = ['', '', sub[['SSS', 'JSS'].index(request.user.profile.class_in[:3])][:5], sub[['SSS', 'JSS'].index(request.user.profile.class_in[:3])][5:]]
                    data = [QSUBJECT.objects.filter(student_id__in=[i.uid for i in eng.order_by('gender', 'uid')], tutor__Class__exact=request.user.profile.class_in, tutor__session__exact=session.profile.session, tutor__subject__in=x).order_by('gender', 'student_id') for x in pag[int(sx)]]
                    if data:
                        ai, bn, cs, dd, ed  = data
                    else:
                        return redirect('home')
                    sumed = round(eng.aggregate(Sum('annual_avr'))['annual_avr__sum'], 1)
                    average = round(eng.aggregate(Avg('annual_avr'))['annual_avr__avg'], 2)
                    cls = str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(request.user.profile.class_in))
                    params = {
                        'subjects':zip(ai, bn, cs, dd, ed), 'Class':request.user.profile.class_in,'request': request, 'today': timezone.now(), 'sum':sumed, 'avg':average, 'term':'BROADSHEET', 'subs':tit[int(sx)], 'myHod':myHod.first(), 'males':eng.filter(gender__exact=1).count(), 'females':eng.filter(gender__exact=2).count(), 'subject_count':5
                        }
                    return Render.render('result/broadsheet.html', params, 'broadsheets/'+str(['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'].index(request.user.profile.class_in))+'/'+cls+sx+session.profile.session, cls+sx+session.profile.session)
                else:
                    return redirect('home')
            else:
                return redirect('home')
        if ty == '5':
            if request.GET.get('saved'):
                params = {
                'request': request, 'today': timezone.now(), 'a':request.GET.get('subject', None), 
                'b':request.GET.get('topic', None), 'c':request.GET.get('sub_topic', None), 'd':request.GET.get('agenda', None), 'e':request.GET.get('class', None), 'f':request.GET.get('lesson_duration', None), 'g':request.GET.get('curriculum_objective', None), 'h':request.GET.get('lesson_objective', None), 'i':request.GET.get('start', None), 'j':request.GET.get('teacher_resources', None), 'k':request.GET.get('student_resources', None), 'l':request.GET.get('preparation', None), 'm':request.GET.get('board', None), 'n':request.GET.get('assignment', None), 'o':request.GET.get('question3', None), 'p':request.GET.get('question2', None), 'q':request.GET.get('question1', None)
                  }
                return Rendered.render('result/lesson_templatepdf.html', params, 'lesson_templates/'+request.user.username, request.user.username)
            return render(request, 'result/lesson_template.html')#lesson_templates
        if ty == '6':
            if request.GET.get('saved'):
                data = [int(request.GET.get(str(i))) for i in range(int(request.GET.get('size'))) if request.GET.get(str(i)) is not None]

                params = {
                'request': request, 'today': timezone.now(), 'Class':request.GET.get('Class', None), 'students':CNAME.objects.filter(id__in=data)
                  }
                return Rendered.render('result/shortlisted.html', params, 'shortlistedVenues/'+request.GET.get('Class', None), request.GET.get('Class', None))
            candi = CNAME.objects.all()
            Class = [i[0] for i in list(set(list(candi.values_list('Class'))))]
            param = {"students":candi.count(), "one":candi.filter(Class__exact='JSS 1', gender__exact=1), "two":candi.filter(Class__exact='JSS 1', gender__exact=2), "three":candi.filter(Class__exact='JSS 2', gender__exact=1), "four":candi.filter(Class__exact='JSS 2', gender__exact=2), "five":candi.filter(Class__exact='JSS 3', gender__exact=1), "six":candi.filter(Class__exact='JSS 3', gender__exact=2), "seven":candi.filter(Class__exact='SSS 1', gender__exact=1), "eight":candi.filter(Class__exact='SSS 1', gender__exact=2), "nine":candi.filter(Class__exact='SSS 2', gender__exact=1), "ten":candi.filter(Class__exact='SSS 2', gender__exact=2), "eleven":candi.filter(Class__exact='SSS 3', gender__exact=1), "tewlve":candi.filter(Class__exact='SSS 3', gender__exact=2)
            }
            return render(request, 'result/exam_venue.html', param)


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
    pair_subject =  ["ACC", "AGR", "ARB", "BIO", "BST", "BUS", "CHE", "CIV", "COM", "CTR", "ECO", "ELE", "ENG", "FUR", "GEO", "GOV", "GRM", "HIS", "ICT", "IRS", "LIT", "MAT", "NAV", "PHY", "PRV", "YOR"]
    Class = ['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', ''][int(pk)]
    response = HttpResponse(content_type=['', 'application/csv', 'application/pdf', 'text/plain', 'text/plain'][int(fm)])
    contents = QSUBJECT.objects.filter(tutor__Class__exact=Class, tutor__subject__exact=pair_subject[int(ps)], tutor__session__exact=session.profile.session).order_by('gender', 'student_name')
    if fm == '4':
        if contents:
            sd = [[x.student_name_id, x.student_name.full_name, randrange(11, 20), randrange(8, 10), randrange(8, 10), randrange(21, 60)] for x in contents]
        else:
            contents = CNAME.objects.filter(Class__exact=Class).order_by('gender', 'full_name')
            sd = [[x.id, x.full_name, randrange(11, 20), randrange(8, 10), randrange(8, 10), randrange(21, 60)] for x in contents]
    elif pk == '6':
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
    response['Content-Disposition'] = "attachment; filename={name}".format(name=Class+[' ', '.csv', '.pdf', '.txt', '.txt'][int(fm)])
    return response 

