from django.contrib.auth.models import User
from .models import QSUBJECT, CNAME, BTUTOR, Edit_User,TUTOR_HOME, QUESTION
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin 
import os
import csv
import datetime
from django.conf import settings
from .utils import do_grades, do_positions, cader, session
from django.http import JsonResponse
from django.http import HttpResponse
session = session()

def Teacher_model_view(request, pk):#
    if request.GET.get('accounts') is not None:
        btutor = get_object_or_404(BTUTOR, pk=pk)
        if request.GET.get('status') == 'delete':
            if btutor.accounts == request.user or request.user.is_superuser == True:
                btutor.delete()
                data = {"status":'object deleted successfully!'}
            else:
                 data = {"status":'Error! Action terminated.'}  
            return JsonResponse(data)
        btutor.accounts = User.objects.get(pk=int(request.GET.get('accounts')))
        btutor.Class, btutor.subject, btutor.first_term, btutor.second_term, btutor.third_term=[request.GET.get(i) for i in ["Class", "Subject", "first_term", "second_term", "third_term"]]
        if btutor.accounts == request.user or request.user.is_superuser == True:
            home = get_object_or_404(TUTOR_HOME, first_term=pk)
            btutor.save()
            home.tutor = btutor.accounts 
            home.save()
        data = {"Class":btutor.Class, "Subject":btutor.subject, "first_term":btutor.first_term, "second_term":btutor.second_term, "third_term":btutor.third_term}
        return JsonResponse(data)
    else:
        form = get_object_or_404(TUTOR_HOME, first_term=pk)
        return render(request, 'result/btutor_form.html', {'home' :TUTOR_HOME.objects.filter(tutor__exact=get_object_or_404(BTUTOR, pk=pk).accounts).order_by('first_term__subject'), 'user' :User.objects.all().order_by('username'), 'caller':form, 'pk':pk})
 
       

class Cname_edit(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = CNAME
    fields = ['full_name', 'gender']
###################################################   

############################################################################### student_in_None
@login_required
def profiles(request, pk):#show single candidate profile
    user=get_object_or_404(User, pk=pk)
    return render(request, 'result/profiles.html', {'qry' : user.profile, 'pk':pk})


class ProfileUpdate(UpdateView):
    model = Edit_User
    fields = ['title', 'first_name', 'last_name', 'bio', 'phone', 'city', 'department', 'location', 'birth_date', 'country', 'organization', 'class_in', 'photo']
    

@login_required
def profile_picture(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST' and request.FILES['myfile']:
        profile = user.profile
        if profile.email_confirmed == True:
            user.last_name = profile.last_name
            user.first_name = profile.first_name
        if profile.photo.name:#if there is file name entry, delete it
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(profile.photo.name))):
                os.remove(os.path.join(settings.MEDIA_ROOT, str(profile.photo.name)))
            else:
                print(f'Error: {os.path.join(settings.MEDIA_ROOT, str(profile.photo.name))} not a valid filename')
        profile.photo = request.FILES['myfile']
        filesize = profile.photo.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*459*571:
            filesize = 'not lager than '+'459'+'*'+'571'+ ' in size'
            return render(request, 'result/file_extension_not_txt.html', {'input': filesize})
        profile.photo.name = request.user.username + '.jpg'
        profile.save()
        return redirect('pro_detail', pk=pk)
    return render(request, 'result/picture.html')  

@login_required
def question_image(request, pk):
    if int(pk) != 0:
        if request.method == 'POST' and request.FILES['myfile']:
            image = QUESTION.objects.get(id=pk)
            image.photo = request.FILES['myfile']
            image.photo.name = image.image_link.split('/')[-1]
            image.image = "True"
            image.save()
            quetions = QUESTION.objects.filter(subjects__exact=image.subjects,classes__exact=image.classes,terms__exact=image.terms, session__exact=image.session)
            return render(request, 'result/quetions.html', {'quetions':quetions, 'Subject':image.subjects, 'Class':image.classes, 'Term':image.terms})
        return render(request, 'result/picture.html')
    else:
        image = QUESTION.objects.get(id=int(request.GET.get('image_ids')))
        image.image = "False"
        image.save()
        data = {'image_status': QUESTION.objects.get(id=request.GET.get('image_ids')).image}
        if data['image_status'] != 'False':
            data['image_empty'] = "Image has been removed successfully."
        return JsonResponse(data)

class Users_update(UpdateView):#New teacher form for every new term, class, subjects
    model = User
    fields = '__all__'
    success_url = reverse_lazy('all_accounts')


def average(x):
    xy = [int(i) for i in x]
    rst = sum(xy)/sum(i > 0 for i in xy)
    if str(rst).split('.')[1] == '5':
        rst = rst + 0.5
    return rst

def get_or_create(tutor, name, scores):#name-name_id
    if len(str(name).split('/')) == 1: 
        student_name = CNAME.objects.get(pk=int(name))
    else:
        student_name = CNAME.objects.get(uid=name)
    instance = QSUBJECT.objects.filter(student_name__exact=student_name, tutor__exact = tutor)
    if not instance.exists():
        instance = QSUBJECT(student_name=student_name, tutor=tutor, test = scores[2], agn = scores[3], atd = scores[4], total = scores[5], exam = scores[6], agr = scores[7], grade = scores[8], posi = scores[9])
    else:
        instance = QSUBJECT.objects.get(student_name=student_name, tutor = tutor)
        if tutor.subject == 'BST1' or tutor.subject == 'BST2':
            instance.test, instance.agn, instance.atd, instance.total, instance.exam, instance.agr, instance.grade, instance.posi = [average([instance.test, scores[2]]), average([scores[3], instance.agn]), average([instance.atd, scores[4]]), average([instance.total, scores[5]]), average([instance.exam, scores[6]]), average([instance.agr, scores[7]]), do_grades([int(average([instance.agr, scores[7]]))], cader(tutor.Class))[0], scores[9]] 
        else:
            instance.test, instance.agn, instance.atd, instance.total, instance.exam, instance.agr, instance.grade, instance.posi = scores[2:]   
    
    instance.updated = datetime.datetime.today()
    instance.save()    
    return instance.student_name.updated

def create_new_subject_teacher(account, Subject, Class, Term): #if not exist.exists():
        new_teacher = BTUTOR(accounts=account, subject = Subject, Class = Class, term = '1st Term', first_term = Term, model_in = 'qsubject', cader=cader(Class), teacher_name = f'{account.profile.title}{account.profile.last_name} : {account.profile.first_name}', session = session.profile.session, updated = datetime.datetime.today())
        new_teacher.save()
        tutors = TUTOR_HOME(tutor = new_teacher.accounts, first_term = new_teacher)
        tutors.save()
        return new_teacher

def currentTerms(Term, tutor):
    if Term == '2nd Term' or Term == '3rd Term':
        if Term == '2nd Term':
            tutor.second_term = Term
            tutor.third_term = '1st Term'
            tutors = TUTOR_HOME.objects.filter(first_term__exact = tutor).first()
            tutors.second_term = tutor
        if Term == '3rd Term':
            tutor.second_term = "2nd Term"
            tutor.third_term = Term
            tutors = TUTOR_HOME.objects.filter(first_term__exact = tutor).first()
            tutors.third_term = tutor
        tutor.save()
        tutors.save()

@login_required
def responsive_updates(request, pk):
    if request.user.is_authenticated:
        if request.user.profile.email_confirmed:
            if pk == '0':#i.student_name.last_name[0]+i.student_name.first_name[0]+'/J/18/'+str(i.student_name.id)      
                if request.GET.get('flow') == "toHtml":#feeding the html page
                    tutor = BTUTOR.objects.get(pk=int(request.GET.get('tutor_id')))
                    instance = QSUBJECT.objects.filter(tutor__exact = tutor).order_by('gender', 'student_id')
                    data = {"status":tutor.updated, "tutor_name":tutor.teacher_name}
                    data["list"] = ['Default']+[[i.student_name.full_name, i.student_name.last_name[0]+i.student_name.first_name[0]+'/J/18/'+str(i.student_name.id), i.test, i.agn, i.atd, i.exam, i.grade, i.posi, i.student_name.gender, i.fagr, i.sagr, i.aagr, i.avr] for i in instance]
                if request.GET.get('flow') == "fromHtml":#fetching from the html page and save to the database.
                    tutor = BTUTOR.objects.get(pk=int(request.user.profile.account_id))
                    response = [get_or_create(tutor, int(request.GET.get('student_id_'+str(i)).split("/")[-1]), [request.GET.get('student_id_'+str(i)), request.GET.get('student_name_'+str(i)), request.GET.get('test_'+str(i)),request.GET.get('agn_'+str(i)),request.GET.get('atd_'+str(i)),request.GET.get('total_'+str(i)), request.GET.get('exam_'+str(i)),request.GET.get('agr_'+str(i)),request.GET.get('grade_'+str(i)),request.GET.get('posi_'+str(i))]) for i in range(int(request.GET.get('start')), int(request.GET.get('end')))]
                    if tutor.subject == 'BST1' or tutor.subject == 'BST2':
                        tutor.subject = 'BST'
                    data = {"status":str(len(response)), 'updated':response}
                    
                if request.GET.get('flow') == "mygrade":
                    tutor = BTUTOR.objects.get(pk=int(request.user.profile.account_id))
                    data = {'grade':do_grades([int(request.GET.get('scores'))], cader(tutor.Class))[0]}

                if request.GET.get('flow') == "currnetTerms":
                    tutor = BTUTOR.objects.all()
                    data = {'tutors':str(len([currentTerms(request.GET.get('Term'), i) for i in tutor]))}
                
                if request.GET.get('flow') == "confirm":
                    exist = BTUTOR.objects.filter(subject__exact = request.GET.get('Subject'), Class__exact = request.GET.get('Class'), term__exact = '1st Term')
                    data = {"status":exist.exists()}
                    if exist.exists(): 
                        tutor = exist.first()
                        if request.GET.get('Term') == '2nd Term' or request.GET.get('Term') == '3rd Term':
                            if request.GET.get('Term') == '2nd Term':
                                tutor.second_term = request.GET.get('Term')
                                tutors = TUTOR_HOME.objects.filter(first_term__exact = exist.first()).first()
                                tutors.second_term = exist.first()
                            if request.GET.get('Term') == '3rd Term':
                                tutor.second_term = "2nd Term"
                                tutor.third_term = request.GET.get('Term')
                                tutors = TUTOR_HOME.objects.filter(first_term__exact = exist.first()).first()
                                tutors.third_term = exist.first()
                            tutor.save()
                            tutors.save()
                        user = request.user.profile
                        user.account_id = exist.first().id
                        user.save()
                        data = {"status":exist.exists(), 'updated':exist.first().updated, "tutor_name":exist.first().teacher_name, "tutor_id":exist.first().id}
                
                if request.GET.get('flow') == "registration":
                    reged = CNAME(full_name = request.GET.get('last').upper() +' '+ request.GET.get('first').upper(), last_name = request.GET.get('last').upper(), middle_name = request.GET.get('middlename').upper(), first_name = request.GET.get('first').upper(), gender = int(request.GET.get('gender')), birth_date = request.GET.get('birth'), Class = request.GET.get('Class'))
                    reged.save()
                    student_id = reged.last_name[0] + reged.first_name[0]+'/'+request.GET.get('Class')[0]+'/'+session.profile.session[-2:]+'/'+str(reged.id)
                    data = {"created":reged.created, "updated":reged.updated, "student_id":student_id}
               
                if request.GET.get('flow') == "admin_no":
                    reged = CNAME.objects.filter(uid__exact=request.GET.get('uid'), full_name__exact=request.GET.get('name'))
                    if reged:
                        data = {"uid":request.GET.get('uid'), "name":request.GET.get('name')}
                    else:
                        if CNAME.objects.filter(uid__exact=request.GET.get('uid')):
                            data = {"exist":1, "name":request.GET.get('name')}
                        else:
                            data = {"exist":0, "name":request.GET.get('name')}
                if request.GET.get('flow') == "create" and request.user.profile.email_confirmed is True:
                        exist = create_new_subject_teacher(request.user, request.GET.get('Subject'), request.GET.get('Class'), request.GET.get('Term'))
                        user = request.user.profile
                        user.account_id = exist.id
                        user.save()
                        data = {"status":exist.id, "tutor_name":exist.teacher_name, "tutor_id":exist.id}
            elif pk == "1":
                    names = QSUBJECT.objects.filter(tutor__Class__exact= request.GET.get('Class'), tutor__subject__exact= request.GET.get('Subject'), tutor__session__exact = session, tutor__term__exact = "1st Term").order_by('gender', 'student_name')
                    data = {"status":str(names.count())}
                    data["list"] = ['Default']+[[i.student_name.full_name, i.student_id] for i in names] 
                    if names.count() == 0:
                        names = CNAME.objects.filter(Class__exact= request.GET.get('Class'), session__exact = session.profile.session).order_by('gender', 'full_name')
                        data = {"status":str(names.count())}
                        data["list"] = ['Default']+[[i.full_name, i.last_name[0]+i.first_name[0]+'/'+i.Class[0]+'/'+i.session[-2:]+'/'+str(i.id)] for i in names]
        else:
            data = {'redirect': 'user/updates/'+str(request.user.profile.id)}
    else:
        data = {"redirect":'home'}
    return JsonResponse(data)

def need_tutor(request, x, subj, Term, username):
    tutor = BTUTOR.objects.filter(subject__exact = subj[0][int(x[1])], Class__exact = subj[1][int(x[0])], term__exact = '1st Term')
    if tutor:
        tutor = tutor.first()
    else:
        user = User.objects.filter(username__exact=username)
        if user:
            account = user.first()
        else:
            account = request.user
        tutor = create_new_subject_teacher(account, subj[0][int(x[1])], subj[1][int(x[0])], Term)
    #ids.append(tutor.id)
    return tutor

def synch(request, last, subject, Class):
    date = datetime.datetime.today()
    subj = [['----', 'ACC', 'AGR', 'ARB', 'BST', 'BIO', 'BUS', 'CTR', 'CHE', 'CIV', 'COM', 'ECO', 'ELE', 'ENG', 'FUR', 'GRM', 'GEO', 'GOV', 'HIS', 'ICT', 'IRS', 'LIT', 'MAT', 'NAV', 'PHY', 'PRV', 'YOR'], ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3']]
    if last == '0' or last == '1' or last == '60':
        if last == '0':#by subject
            new = QSUBJECT.objects.filter(tutor__subject__exact=subj[0][int(subject)], tutor__Class__exact=subj[1][int(Class)]).order_by('gender', 'student_name__full_name')            
        elif last == '1':#by class
            new = QSUBJECT.objects.filter(tutor__Class__exact=subj[1][int(Class)]).order_by('tutor__subject')
        else:# in minute 
            new = QSUBJECT.objects.filter(updated__year__exact=date.year, updated__month__exact=date.month, updated__day__exact=date.day, updated__hour__exact=date.hour, updated__minute__range=[0, 60])# in minutes
        data = {'response':[[i.student_name.uid.strip(), i.tutor.subject_teacher_id, i.test, i.agn, i.atd, i.total, i.exam, i.agr, i.grade, i.posi, i.tutor.accounts.username] for i in new]}
    elif last == '2':   
        data = {'id':str(need_tutor(request, request.GET.get('subject_code_0').split('-'), subj, request.GET.get('Term'), request.GET.get('username')).id), 'response':[get_or_create(need_tutor(request, request.GET.get('subject_code_'+str(i)).split('-'), subj, request.GET.get('Term'), request.GET.get('username')),  request.GET.get('uid_'+str(i)), [request.GET.get('uid_'+str(i)), request.GET.get('uid_'+str(i)), request.GET.get('test_'+str(i)),request.GET.get('agn_'+str(i)),request.GET.get('atd_'+str(i)),request.GET.get('total_'+str(i)), request.GET.get('exam_'+str(i)),request.GET.get('agr_'+str(i)),request.GET.get('grade_'+str(i)),request.GET.get('posi_'+str(i))]) for i in range(0, int(request.GET.get('end'))) if request.GET.get('uid_'+str(i)) in [x.uid for x in CNAME.objects.all()]]}
    return JsonResponse(data)