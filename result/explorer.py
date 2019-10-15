from .models import ANNUAL, OVERALL_ANNUAL#, SESSION#, ASUBJECTS
from django.shortcuts import render, redirect, get_object_or_404
from result.utils import do_grades, do_positions, cader, session
from datetime import datetime
from django.db.models import Sum, Avg
from datetime import timedelta
from django.contrib import messages
import time
from statistics import mean
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
 #return HttpResponse(student_name_id_third, content_type='text/plain')#

session = session()

dim = []                        
def return_value_or_None(request, pk, x):
    name = ANNUAL.objects.get(id=pk)
    mod = ANNUAL.objects.select_related('student_name').filter(student_name__exact=name.student_name, subject_by__Class__exact=request.user.profile.class_in, subject_by__session__exact=session, subject_by__subject__name__in=x)
    if mod.count() == 1:#do subject with only one return
        item = ANNUAL.objects.select_related('student_name').get(student_name=name.student_name, subject_by__Class=request.user.profile.class_in, subject_by__session=session, subject_by__subject__name__in=x)
        dim.append(item.Agr)
        return item 
    else:
        return None


def create_student_annual(request):
        global dim
        trace = [['CHE', 'ACC', 'ARB'], ['GOV', 'ICT', 'HIS'], ['GEO', 'AGR', 'YOR'], ['BST', 'BIO', 'ECO'], ['BUS', 'PHY', 'LIT', 'COM'], ['ELE', 'CTR', 'GRM', 'PRV']]
        annuals = ANNUAL.objects.select_related('subject_by').filter(subject_by__subject__name__exact= 'ENG', subject_by__Class__exact=request.user.profile.class_in, subject_by__session__exact = session)
        if len(annuals) != 0:
            ids = [x for x in list(annuals.values_list('id'))]
            c, j = [None, None]
            for r in range(0, len(ids)):
                name = ANNUAL.objects.get(id=ids[r][0])
                a = return_value_or_None(request, ids[r][0], trace[0])
                b = return_value_or_None(request, ids[r][0], trace[1])
                if name.subject_by.Class== 'SSS 1' or name.subject_by.Class== 'SSS 2' or name.subject_by.Class== 'SSS 3':#yor
                    c = return_value_or_None(request, ids[r][0], trace[2])
                d = return_value_or_None(request, ids[r][0], trace[3])
                e = return_value_or_None(request, ids[r][0], trace[4])   
                f = return_value_or_None(request, ids[r][0], trace[5])
                #['MAT', 'NAV', 'IRS', 'AGR'] ['MAT', 'CIV', 'IRS']
                g = return_value_or_None(request, ids[r][0], ['MAT'])
                h = return_value_or_None(request, ids[r][0], ['CIV', 'NAV'])
                i = return_value_or_None(request, ids[r][0], ['IRS'])     
                if name.subject_by.Class== 'JSS 1' or name.subject_by.Class== 'JSS 2' or name.subject_by.Class== 'JSS 3':#agr
                    c = return_value_or_None(request, ids[r][0], ['YOR'])
                    j = return_value_or_None(request, ids[r][0], ['AGR'])            #i
                if len(dim) != 0:
                    OVERALL_ANNUAL.objects.create(student_name=name.student_name, class_in=name.subject_by.Class, teacher_in=request.user,  session=name.subject_by.session, acc = a, ict = b, yor = c, bst = d, bus = e, prv = f, eng = name, mat = g, nva = h, irs = i, agr = j, AGR = round(sum(dim),2), AVR = round(mean(dim),2), GRD = do_grades([int(mean(dim))], cader(get_object_or_404(ANNUAL, pk=ids[r][0]).third.tutor.Class))[0]).save()
                dim = []  
        else:
             return redirect('home')


def subject_counter(request):
    acc = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, acc__third__tutor__subject__name__exact=x).count()) for x in ['CHE', 'ACC', 'ARB']]
    ict = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, ict__third__tutor__subject__name__exact=x).count()) for x in ['GOV', 'ICT']]
    yor = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, yor__third__tutor__subject__name__exact=x).count()) for x in ['GEO', 'AGR', 'YOR']]
    bst = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, bst__third__tutor__subject__name__exact=x).count()) for x in ['ECO', 'BIO']]
    bus = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, bus__third__tutor__subject__name__exact=x).count()) for x in ['PHY', 'LIT', 'COM']]
    prv = [x+':'+ str(OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session, prv__third__tutor__subject__name__exact=x).count()) for x in ['ELE', 'CTR', 'GRM']]
    return sorted([acc,ict,yor,bst,bus,prv])
    
def broad_sheet(request):
    start_time = time.time()
    over = OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session)
    annuals = ANNUAL.objects.select_related('subject_by').filter(subject_by__subject__name__exact= 'ENG', subject_by__Class__exact=request.user.profile.class_in, subject_by__session__exact = session)
    if over.count() != annuals.count():
        if over.count() == 0:
            create_student_annual(request)
        else:
            over.delete()
            create_student_annual(request)
        al = OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session).order_by('order')
        if al.count() != 0:
            annual_id = [list(x) for x in list(al.values_list('id', 'AVR')) if x != None]
            posi = do_positions([x[1] for x in annual_id])
            for i in range(0, len(annual_id)):
                get = get_object_or_404(OVERALL_ANNUAL, pk=annual_id[i][0])
                get.POS = posi[i]
                get.order = posi[i].split(posi[i][-2:])[0]
                get.save()
            elapsed_time_secs = time.time() - start_time
            msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
            messages.success(request, msg)
            print(msg)
            if request.user.profile.class_in.split(' ')[0] == 'JSS':
                return render(request, 'result/display_sheet_j.html',  {'msg':msg, 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2), 'date': datetime.now(), 'mains': al.order_by('order'),  'class_in':request.user.profile.class_in, 'counts':al.count()})
            else:
                return render(request, 'result/display_sheet.html',  {'msg':msg, 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2), 'date': datetime.now(), 'mains': al.order_by('order'),  'class_in':request.user.profile.class_in, 'counts':al.count()})

        else:
            return redirect('home')
    
    else:
        al = OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session)
        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
        messages.success(request, msg)
        print(msg)
        if request.user.profile.class_in.split(' ')[0] == 'JSS':
            return render(request, 'result/display_sheet_j.html',  {'msg':msg, 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2), 'date': datetime.now(), 'mains': al.order_by('order'),  'class_in':request.user.profile.class_in, 'counts':al.count()})
        else:
            return render(request, 'result/display_sheet.html',  {'msg':msg, 'overall':round(al.aggregate(Sum('AGR'))['AGR__sum'], 1), 'per':round(al.aggregate(Avg('AVR'))['AVR__avg'],2), 'date': datetime.now(), 'mains': al.order_by('order'),  'class_in':request.user.profile.class_in, 'counts':al.count()})


@login_required
def reload(request):
    if request.user.profile.class_in != None:
        sd = OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=request.user, class_in__exact=request.user.profile.class_in, session__exact=session).delete()
        print('previouse' +str(sd)+ 'records deleted.')
        return redirect('broadsheet_last_stage')
    else:
        return redirect('home')

    
def broadsheet_pdf(request, pk):
    from django.contrib.auth.models import User
    al = OVERALL_ANNUAL.objects.select_related('teacher_in').filter(teacher_in__exact=User.objects.get(pk=pk), class_in__exact=User.objects.get(pk=pk).profile.class_in, session__exact=session)
    return render(request, 'result/broadsheet_pdf.html',  {'mains': al.order_by('order')})
  
