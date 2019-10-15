######################STAGE 2 ::: UPLOAD SCORES##################STARTS
from .forms import new_student_name, student_name
from collections import Counter
from .models import QSUBJECT, CNAME, BTUTOR, ASUBJECTS, ANNUAL, REGISTERED_ID, TUTOR_HOME
from django.shortcuts import render, redirect, get_object_or_404
from result.utils import do_grades, do_positions, cader
from django.contrib.auth.decorators import login_required
import time
from django.contrib.auth.models import User
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
import os
import shutil


from result.utils import session
session = session()

def bst1_plus_bst2(dim):
    result = []
    for i in range(0, len(dim)):
        result += [[int(round((sum(dim[i][0:2])/sum(x > 0 for x in dim[i][0:2])+0.1), 0)), int(round((sum(dim[i][2:4])/sum(x > 0 for x in dim[i][2:4])+0.1), 0)), int(round((sum(dim[i][4:6])/sum(x > 0 for x in dim[i][4:6])+0.1), 0)), int(round((sum(dim[i][6:8])/sum(x > 0 for x in dim[i][6:8])+0.1), 0))]]
    return result 

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

@login_required
def upload_new_subject_scores(request, pk):
    start_time = time.time()
    tutor = get_object_or_404(BTUTOR, pk=pk) 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            return render(request, 'result/file_extension_not_txt.html')
        file_txt = my_file.read().decode("ISO-8859-1")
        if tutor.term == '3rd Term':
            if len(set([i[0] for i in[x for x in list(QSUBJECT.objects.filter(tutor__Class__exact = tutor.Class, tutor__subject__exact = tutor.subject, tutor__session__exact = tutor.session).values_list('tutor'))]])) != 2:
                return redirect('home')
        contents = file_txt.split('\n');
        named_scores = [[], [], []]#[compltet_data_for_each_student, scores, name_only]
        for line in contents:
            each_student = [new.strip() for new in line.split(',')]
            named_scores[0] += [each_student]
        serial_no = [named_scores[0].index(x) for x in named_scores[0]]#get name indexes
        valid_input = [n[:] for n in named_scores[0] if len(n) > 2]
        males = serial_no[-1]#last_no on male list
        females = len(valid_input) - males
        tutor.males = males
        tutor.females = females
        
        #####################REPEATED NAMES######################################
        word_counts = Counter([r[0] for r in valid_input])
        repeated_name = word_counts.most_common()
        ideces = [list(x) for x in repeated_name if x[1] != 1]
        for i in range(0, len(ideces)):
            repeated_names = [valid_input[valid_input.index(x)][0] + str(valid_input.index(x)) for x in valid_input if x[0] == ideces[i][0]]
            each = [valid_input.index(x) for x in valid_input if x[0] == ideces[i][0]]
            for r in range(0, len(repeated_names)):
                valid_input[each[r]] = str(repeated_names[r])
        
        ##########################ERROR CHECK##############################
        sd = []
        for i in range(0, len(valid_input)):
            output = [check(s) for s in valid_input[i]]
            if len(output) == 9:
                if output != [False, True, True, True, True, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id})
            elif len(output) == 5:
                if output != [False, True, True, True, True]:
                    return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id})
            else:
                return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id}) 
        ##########################ERROR CHECK##############################
            sd += [[valid_input[i][0]]+[[int(float(ints)) for ints in valid_input[i][1:]]][0]]
        
        if len(sd) == 9:#BST ONLY: Reduced 8 to 4 columns by averaging.
            from statistics import mean
            valid_input = [[round(mean(x[1:3])), round(mean(x[3:5])), round(mean(x[5:7])), round(mean(x[7:9]))] for x in sd]
        else:
            valid_input = sd
            
        x = cader(tutor.Class)
        raw_scores = [[x[0], x[1], x[2], x[3], sum(x[1:4]), x[4], sum([sum(x[1:4]), x[4]])] for x in valid_input]
        
        posi = do_positions([int(i[-1]) for i in raw_scores][:])
        grade = do_grades([int(i[-1]) for i in raw_scores][:], x)
        
        
        #####################NAMES QUERIES######################################
        Genders = [sorted(raw_scores[:males]), sorted(raw_scores[males:])]#sorted_list
        for i in range(0, 2):
            splited = sorted([x[0].split(' ') for x in Genders[i]])
            for r in range(0, len(splited)):
                unspaced = [i for i in splited[r] if len(i) > 2]+['first_name']
                Genders[i][r][0] = unspaced[0] +" "+ unspaced[1]
        Males = [[list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name', 'id'))], sorted([x for x in [x[0] for x in Genders[0]] if x not in [x[0] for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name'))]])]
        [[CNAME(full_name = i, gender = 1).save() for i in Males[1] if len(Males[1]) != 0]]#remainder
        if len(Males[1]) != 0:
            Males[0] + [list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name', 'id'))][0]

        Females = [[list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name', 'id'))], sorted([x for x in [x[0] for x in Genders[1]] if x not in [x[0] for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name'))]])]
        [[CNAME(full_name = i, gender = 2).save() for i in Females[1] if len(Females[1]) != 0]]#remainder
        if len(Females[1]) != 0:
            Females[0] + [list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name', 'id'))][0]
        
        
        Both_sex_scores = Genders[0] + Genders[1]
               
        final = [x+[y]+[z] for x,y,z in zip(Both_sex_scores, grade, posi)]#complete scores
        Both_sex_ids = sorted(Males[0], key=sort_key) + sorted(Females[0], key=sort_key)#compltes ids 
        joined_scores_ids = [[str(i[1])]+x[:] for i,x in zip(Both_sex_ids, final)]
        #from django.http import HttpResponse
        #return HttpResponse([len(joined_scores_ids)], content_type='text/plain')#
                                     ########################QUERY SUBJECT MODEL FOR CONTINUATIONS###############################
        
        Both_sex_ids_final = [x for x in joined_scores_ids if x[1] not in [r[0] for r in [list(QSUBJECT.objects.filter(student_name__in=CNAME.objects.filter(full_name__in=[x[1] for x in joined_scores_ids])).distinct().values_list('student_name'))]]]
        
        [QSUBJECT(student_name=CNAME.objects.get(pk=i[0]), test=i[2], agn=i[3], atd=i[4], exam=i[6], total=i[5], agr=i[7], posi=i[9], grade=i[8], tutor = tutor, cader = x).save() for i in Both_sex_ids_final]
        elapsed_time_secs = time.time() - start_time
        msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
        messages.success(request, msg)
        print(msg)
        tutor.save()
        if tutor.term == '3rd Term':
            qs = QSUBJECT.objects.select_related('tutor').filter(tutor__id__exact=pk)
            [ANNUAL(student_name = x.student_name, third = x, subject_by = BTUTOR.objects.get(pk=pk)).save() for x in qs]
    else:#
        return render(request, 'result/loader.html', {'pk':pk, 'qry':tutor})
    ######################STAGE 2 ::: UPLOAD SCORES##################ENDS
    return redirect('subject_view', pk=pk)#summarise all tutor's uploads
###############################################################################
###



basepath = settings.MEDIA_ROOT + '/upload'
reloadpath = settings.MEDIA_ROOT + '/reload'
def mass_upload(request):
    start_time = time.time()
    for entry in os.listdir(basepath):#6 entries {JSS1, JSS 2, JSS 3, SSS 1, SSS 2, SSS 3}
        for files in os.listdir(os.path.join(basepath, entry)): #33 + 60
            os.chdir(os.path.join(basepath, entry))
            with open(files, 'r') as file:
                new = files.split("_")#['99', 'SSS 3', '3', 'MAT.txt']
                user = User.objects.get(pk=int(new[0]))#99   'MAT'                     'SSS 3'                                                     '3rd Term'                 's'
                unique = BTUTOR.objects.filter(accounts__exact=user, term__exact=['empty', '1st Term', '2nd Term', '3rd Term'][int(new[2])], Class__exact=new[1], subject__exact = ASUBJECTS.objects.get(name=new[-1].split('.')[0]), session__exact = session)
                if unique.count() == 0:
                    tutor = BTUTOR(accounts=user, subject = ASUBJECTS.objects.get(name=new[-1].split('.')[0]), Class = new[1], term = ['empty', '1st Term', '2nd Term', '3rd Term'][int(new[2])], cader=cader(new[1]), teacher_name = f'{user.profile.title}{user.profile.last_name} : {user.profile.first_name}', session = session)
                    tutor.save()
                else:
                    tutor = BTUTOR.objects.get(accounts=user, term=['empty', '1st Term', '2nd Term', '3rd Term'][int(new[2])], Class=new[1], subject = ASUBJECTS.objects.get(name=new[-1].split('.')[0]), session = session)
                
                file_txt = file.read()#.decode("ISO-8859-1")
                contents = file_txt.split('\n');
                named_scores = [[], [], []]#[compltet_data_for_each_student, scores, name_only]
                for line in contents:
                    each_student = [new.strip() for new in line.split(',')]
                    named_scores[0] += [each_student]
                serial_no = [named_scores[0].index(x) for x in named_scores[0]]#get name indexes
                valid_input = [n[:] for n in named_scores[0] if len(n) > 2]
                males = serial_no[-1]#last_no on male list
                females = len(valid_input) - males
                tutor.males = males
                tutor.females = females
                tutor.save()
                #####################REPEATED NAMES######################################
                word_counts = Counter([r[0] for r in valid_input])
                repeated_name = word_counts.most_common()
                ideces = [list(x) for x in repeated_name if x[1] != 1]
                for i in range(0, len(ideces)):
                    repeated_names = [valid_input[valid_input.index(x)][0] + str(valid_input.index(x)) for x in valid_input if x[0] == ideces[i][0]]
                    each = [valid_input.index(x) for x in valid_input if x[0] == ideces[i][0]]
                    for r in range(0, len(repeated_names)):
                        valid_input[each[r]] = str(repeated_names[r])
                
                ##########################ERROR CHECK##############################
                sd = []
                for i in range(0, len(valid_input)):
                    output = [check(s) for s in valid_input[i]]
                    if len(output) == 9:
                        if output != [False, True, True, True, True, True, True, True, True]:
                            return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':ASUBJECTS.objects.get(name=new[-1].split('.')[0])})
                    elif len(output) == 5:
                        if output != [False, True, True, True, True]:
                            return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':ASUBJECTS.objects.get(name=new[-1].split('.')[0])})
                    else:
                        return render(request, 'result/InputTypeError.html', {'int':i, 'invalid': valid_input[i], 'pk':tutor.id, 'subject':ASUBJECTS.objects.get(name=new[-1].split('.')[0])}) 
                ##########################ERROR CHECK##############################
                    sd += [[valid_input[i][0]]+[[int(float(ints)) for ints in valid_input[i][1:]]][0]]
                
                if len(sd) == 9:#BST ONLY: Reduced 8 to 4 columns by averaging.
                    from statistics import mean
                    valid_input = [[round(mean(x[1:3])), round(mean(x[3:5])), round(mean(x[5:7])), round(mean(x[7:9]))] for x in sd]
                else:
                    valid_input = sd
                    
                x = cader(tutor.Class)
                raw_scores = [[x[0], x[1], x[2], x[3], sum(x[1:4]), x[4], sum([sum(x[1:4]), x[4]])] for x in valid_input]
                
                posi = do_positions([int(i[-1]) for i in raw_scores][:])
                grade = do_grades([int(i[-1]) for i in raw_scores][:], x)
                
                
                #####################NAMES QUERIES######################################
                Genders = [sorted(raw_scores[:males]), sorted(raw_scores[males:])]#sorted_list
                for i in range(0, 2):
                    splited = sorted([x[0].split(' ') for x in Genders[i]])
                    for r in range(0, len(splited)):
                        unspaced = [i for i in splited[r] if len(i) > 2]+['first_name']
                        Genders[i][r][0] = unspaced[0] +" "+ unspaced[1]
                Males = [[list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name', 'id'))], sorted([x for x in [x[0] for x in Genders[0]] if x not in [x[0] for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name'))]])]
                [[CNAME(full_name = i, gender = 1).save() for i in Males[1] if len(Males[1]) != 0]]#remainder
                if len(Males[1]) != 0:
                    Males[0] + [list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[0]]).values_list('full_name', 'id'))][0]
        
                Females = [[list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name', 'id'))], sorted([x for x in [x[0] for x in Genders[1]] if x not in [x[0] for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name'))]])]
                [[CNAME(full_name = i, gender = 2).save() for i in Females[1] if len(Females[1]) != 0]]#remainder
                if len(Females[1]) != 0:
                    Females[0] + [list(x) for x in list(CNAME.objects.filter(full_name__in=[x[0] for x in Genders[1]]).values_list('full_name', 'id'))][0]
                
                
                Both_sex_scores = Genders[0] + Genders[1]
               
                final = [x+[y]+[z] for x,y,z in zip(Both_sex_scores, grade, posi)]#complete scores
                Both_sex_ids = sorted(Males[0], key=sort_key) + sorted(Females[0], key=sort_key)#compltes ids 
                joined_scores_ids = [[str(i[1])]+x[:] for i,x in zip(Both_sex_ids, final)]
                                             ########################QUERY SUBJECT MODEL FOR CONTINUATIONS###############################
                
                Both_sex_ids_final = [x for x in joined_scores_ids if x[1] not in [r[0] for r in [list(QSUBJECT.objects.filter(student_name__in=CNAME.objects.filter(full_name__in=[x[1] for x in joined_scores_ids])).distinct().values_list('student_name'))]]]
                
                [QSUBJECT(student_name=CNAME.objects.get(pk=i[0]), test=i[2], agn=i[3], atd=i[4], exam=i[6], total=i[5], agr=i[7], posi=i[9], grade=i[8], tutor = tutor, cader = x).save() for i in Both_sex_ids_final]
                elapsed_time_secs = time.time() - start_time
                msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
                messages.success(request, msg)
                print(msg)
                tutor.save()
                if tutor.term == '3rd Term':
                    qs = QSUBJECT.objects.select_related('tutor').filter(tutor__id__exact=tutor.id)
                    [ANNUAL(student_name = x.student_name, third = x, subject_by = BTUTOR.objects.get(pk=tutor.id)).save() for x in qs]                    
                    #agr = [r[0] for r in [x[:] for x in list(ANNUAL.objects.filter(subject_by__exact=tutor).values_list('Agr'))]]###############news
                    agr = [r[0] for r in [x[:] for x in list(ANNUAL.objects.filter(subject_by__exact=tutor).values_list('Agr'))]]###############news
                    posi = do_positions(agr[:])
                    ids = [r[0] for r in [x[:] for x in list(ANNUAL.objects.filter(subject_by__exact=tutor).values_list('id'))]]
                    for i in range(0, len(agr)):
                        objs = ANNUAL.objects.get(pk=ids[i])
                        objs.grade = do_grades([int(objs.Agr)], cader(tutor.Class))[0]
                        objs.Posi = posi[i]
                        objs.save()
                    objs = ANNUAL.objects.get(pk=ids[0])
                    TUTOR_HOME(tutor = objs.first.tutor.accounts, teacher_name = objs.first.tutor.teacher_name, first_term = objs.first.tutor, second_term = objs.second.tutor, third_term = objs.third.tutor).save()
                elapsed_time_secs = time.time() - start_time
                msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
                messages.success(request, msg)
                print(msg)
                file.close()
                new_file = os.path.join(os.path.join(reloadpath, entry), files)
                old_file = os.path.join(os.path.join(basepath, entry), files)
                shutil.move(old_file, new_file)

    ######################STAGE 2 ::: UPLOAD SCORES##################ENDS
    return redirect('home')

@login_required
def search_to_load(request, pk):
    if request.method == 'POST':
        result =  new_student_name(request.POST)
        if result.is_valid():
            reg = REGISTERED_ID.objects.filter(student_name__in=CNAME.objects.filter(last_name__icontains = result.cleaned_data['student_name'].upper()), session__exact=session)
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

def upload_a_name(request, pk):
    if request.method == 'POST':
        result = student_name(request.POST)
        if result.is_valid():
            new_name = CNAME(full_name=result.cleaned_data['last_name'].upper()+' '+result.cleaned_data['first_name'].upper(), gender=result.cleaned_data['gender'])#adding new student_name
            new_name.save()
            a_student = QSUBJECT(student_name=new_name, tutor=BTUTOR.objects.get(pk=pk))
            a_student.save()
            return redirect('subject_updates_model', pk = a_student.id)
    else:
        result = student_name()
    return render(request, 'result/a_student_name.html', {'result': result})

############################################################################