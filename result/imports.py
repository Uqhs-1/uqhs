######################STAGE 2 ::: UPLOAD SCORES##################STARTS
from .forms import new_student_name, student_name
from collections import Counter
from .models import QSUBJECT, CNAME, BTUTOR, ASUBJECTS, ANNUAL, REGISTERED_ID, TUTOR_HOME, QUESTION, STUDENT_INFO
from django.shortcuts import render, redirect, get_object_or_404
from .utils import do_grades, do_positions, cader, round_half_up, session
from django.contrib.auth.decorators import login_required
import time
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
import os
import shutil
from statistics import mean
from django.http import JsonResponse
#import datetime

session = session()

def check(inp):
    try:
        inp = inp.replace(',', '.')
        num_float = float(inp)
        num_int = int(num_float)
        return num_int == num_float
    except ValueError:
        return False
    
def sort_key(dim):#sort with first elements of the list
    return dim[0]

def check_repeated_names(valid_input):
    word_counts = Counter([r[0] for r in valid_input])
    repeated_name = word_counts.most_common()
    ideces = [list(x) for x in repeated_name if x[1] != 1]
    for i in range(0, len(ideces)):
        repeated_names = [valid_input[valid_input.index(x)][0] + str(valid_input.index(x)) for x in valid_input if x[0] == ideces[i][0]]
        each = [valid_input.index(x) for x in valid_input if x[0] == ideces[i][0]]
        for r in range(0, len(repeated_names)):
            valid_input[each[r]][0] = str(repeated_names[r])
    return valid_input


def trim(Genders):
    splited = sorted([x[0].split(' ') for x in Genders])
    for r in range(0, len(splited)):
        unspaced = [i for i in splited[r] if len(i) > 2]
        Genders[r][0] = unspaced[0] +" "+ unspaced[1]
    return Genders  


@login_required
def upload_new_subject_scores(request, pk):
    start_time = time.time()
    tutor = get_object_or_404(BTUTOR, pk=pk) 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html')
        file_txt = my_file.read().decode("ISO-8859-1")
        contents = file_txt.split('\n');
        named_scores = [[], [], []]#[compltet_data_for_each_student, scores, name_only]
        for line in contents:
            each_student = [new.strip() for new in line.split(',')]
            named_scores[0] += [each_student]
        valid_input = [n[:] for n in named_scores[0] if len(n) > 2]
        #####################REPEATED NAMES######################################
        valid_input = check_repeated_names(valid_input)
        ##########################ERROR CHECK##########
        for i in range(0, len(valid_input)):
            output = [check(s) for s in valid_input[i]]
            if len(output) == 9:
                if output != [False, True, True, True, True, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject.name})
            elif len(output) == 5:
                if output != [False, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject.name})
            else:
                return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':tutor.subject.name})
        if not QSUBJECT.objects.filter(tutor__subject__name__exact='BST', tutor__Class__exact=tutor.Class, tutor__first_term__exact='1st Term', tutor__session__exact=tutor.session): 
            if len(valid_input[0]) == 9:#BST ONLY: Reduced 8 to 4 columns by averaging.
                valid_input = [[x[0], round_half_up(mean([int(i) for i in x[1:3]])), round_half_up(mean([int(i) for i in x[3:5]])), round_half_up(mean([int(i) for i in x[5:7]])), round_half_up(mean([int(i) for i in x[7:9]]))] for x in valid_input]
        x = cader(tutor.Class)
        raw_scores = [[x[0], int(x[1]), int(x[2]), int(x[3]), sum([int(i) for i in x[1:4]]), int(x[4]), sum([sum([int(i) for i in x[1:4]]), int(x[4])])] for x in valid_input]
        trimedNames = trim(raw_scores)
        posi = do_positions([int(i[-1]) for i in trimedNames][:])
        grade = do_grades([int(i[-1]) for i in trimedNames][:], x)
        final = [x+[y]+[z] for x,y,z in zip(trimedNames, grade, posi)]
        from .updates import get_or_create
        [get_or_create(tutor, i[0], i) for i in final if CNAME.objects.filter(full_name__exact=i[0]).exists()]
        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
        messages.success(request, msg)
        print(msg)
    else:#
        return render(request, 'result/loader.html', {'pk':pk, 'qry':tutor})
    ######################STAGE 2 ::: UPLOAD SCORES##################ENDS
    return redirect('subject_view', pk=pk, md=1)#summarise all tutor's uploads
###############################################################################
###
def setup_questions(request): 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html')
        file_txt = my_file.read().decode("ISO-8859-1")
        text = file_txt.split('_')
        crop = [i.split('\t') for i in text]
        valid = [i for i in crop if len(i) == 2]
        if len(valid) % 6 == 0:
            filterd = [[i[1] for i in valid if len(i) == 2][i*6:(i+1)*6] for i in range((len([i[1] for i in valid if len(i) == 2])+6-1)//6)]
            serial_no = [i+1 for i in range(len(filterd))]
            [QUESTION(subjects=request.POST.get('Subject', False),classes=request.POST.get('Class', False),terms=request.POST.get('Term', False),question=i[0],optionA=i[1],optionB=i[2],optionC=i[3],optionD=i[4],CORRECT=i[5], comment=i[5], serial_no=r, session=session).save() for i,r in zip(filterd,serial_no) if len(i) == 6]
        else:
            from django.http import HttpResponse
            return HttpResponse([valid], content_type='text/plain')#
    else:#
        return render(request, 'result/question_loader.html')
    return redirect('home') 

@login_required
def search_to_load(request, pk):
    if request.method == 'POST':
        result =  new_student_name(request.POST)
        if result.is_valid():
            reg = REGISTERED_ID.objects.filter(student_name__in=CNAME.objects.filter(last_name__icontains = result.cleaned_data['student_name']), session__exact=session)
            return render(request, 'result/searched_names.html',  {'all_page' : reg}) 
    else:
        result = new_student_name()
    return render(request, 'result/existing_name.html', {'result': result, 'pk': pk})

def upload_a_score(request, pk):
    exist_student = QSUBJECT(student_name=CNAME.objects.get(pk=pk))
    exist_student.save() 
    return redirect('subject_updates_model', pk=exist_student.id)


def annual_reload(request, pk):
    an = ANNUAL.objects.select_related('subject_by').filter(subject_by__id__exact=pk).delete()
    print('previous'+str(an)+'deleted!')
    qs = QSUBJECT.objects.select_related('tutor').filter(tutor__id__exact=pk)
    [ANNUAL(student_name = x.student_name, third = x, subject_by = BTUTOR.objects.get(pk=pk)).save() for x in qs]
    return redirect('position_updates', pk=pk, term=4)

def add_annual_score(request, pk):
    get_student = QSUBJECT.objects.get(pk=pk) 
    if QSUBJECT.objects.select_related('student_id').filter(student_id__exact=get_student.student_id, tutor__subject__exact=get_student.tutor.subject, tutor__Class__exact=get_student.tutor.Class, tutor__term__exact='1st Term', tutor__session__exact=get_student.tutor.session).count() != 0:
        first = QSUBJECT.objects.get(student_id=get_student.student_id, tutor__subject=get_student.tutor.subject, tutor__Class=get_student.tutor.Class, tutor__term='1st Term', tutor__session=get_student.tutor.session)
    else:
        first = None
    if QSUBJECT.objects.select_related('student_id').filter(student_id__exact=get_student.student_id, tutor__subject__exact=get_student.tutor.subject, tutor__Class__exact=get_student.tutor.Class, tutor__term__exact='2nd Term', tutor__session__exact=get_student.tutor.session).count() != 0:
        second = QSUBJECT.objects.get(student_id=get_student.student_id, tutor__subject=get_student.tutor.subject, tutor__Class=get_student.tutor.Class, tutor__term='2nd Term', tutor__session=get_student.tutor.session)
    else:
        second = None
    annual = ANNUAL(subject_by = get_student.tutor, student_name=get_student.student_name, first = first, second=second, third = get_student)
    annual.save() 
    return redirect('position_updates', pk=get_student.tutor.id, term=4)

def upload_a_name(request, s, pk):
    if request.GET.get('last') and request.GET.get('first') and request.GET.get('gender') and request.GET.get('birth'):
        if CNAME.objects.filter(full_name__exact=request.GET.get('last')+' '+request.GET.get('first')):
            edit = CNAME.objects.get(full_name=request.GET.get('last')+' '+request.GET.get('first'))
        else:
            edit = CNAME.objects.get(full_name='Surname')
        edit.full_name, edit.gender, edit.birth_date = request.GET.get('last')+' '+request.GET.get('first'), request.GET.get('gender'), request.GET.get('birth')#adding new student_name
        edit.save()
        if int(s) > 2:
            if QSUBJECT.objects.filter(student_name__exact=edit, tutor__exact=BTUTOR.objects.get(pk=int(s))).exists():
                data = {"status":edit.full_name+' records updated.', "pk":QSUBJECT.objects.get(student_name=edit, tutor=BTUTOR.objects.get(pk=int(s))).id, 'birth':edit.birth_date}
            else:
                a_student = QSUBJECT(student_name=edit, tutor=BTUTOR.objects.get(pk=int(s)))
                a_student.save()
                data = {"status":edit.full_name+' records updated.', "id":a_student.id, 'birth':edit.birth_date}
        else:
            data = {"status":edit.full_name+' record updated successfully.', 'birth':edit.birth_date}
        return JsonResponse(data) 
    if int(pk) == 0:#new name registration
        if not CNAME.objects.filter(birth_date__exact= '2000-10-01'):
            cname = CNAME(gender=1)
            cname.save()
        else:
            cname = CNAME.objects.filter(birth_date__exact= '2000-10-01').first()
    else:
        cname = CNAME.objects.get(pk=pk)#edit old
    return render(request, 'result/a_student_name.html', {"pk":pk, 's':s, 'cname':cname})   
    


