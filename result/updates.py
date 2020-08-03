from django.contrib.auth.models import User
from .models import QSUBJECT, CNAME, BTUTOR, Edit_User,TUTOR_HOME, QUESTION
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin 
import os
from django.conf import settings
from .utils import do_grades, do_positions, cader, session
from django.http import JsonResponse
from statistics import mean  
from .creates import create_new_subject_teacher
session = session()

class Teacher_model_view(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = BTUTOR
    fields = ['accounts', 'teacher_name', 'subject', 'Class', 'term', 'males', 'females', 'teacher_in', 'status', 'first_term', 'second_term', 'third_term']
    #success_url = reverse_lazy('home') 
    
    
class tutor_home_view(UpdateView):
    model = TUTOR_HOME
    fields = ['tutor', 'teacher_name', 'first_term', 'second_term', 'third_term']#, 'males', 'females', 'teacher_in', 'status']    


class Cname_edit(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = CNAME
    fields = ['full_name', 'gender']
###################################################   

############################################################################### student_in_None
@login_required
def profiles(request, pk):#show single candidate profile
    qry = get_object_or_404(Edit_User, user=get_object_or_404(User, pk=pk))
    return render(request, 'result/profiles.html', {'qry' : qry, 'pk':pk})


class ProfileUpdate(UpdateView):
    model = Edit_User
    fields = ['title', 'first_name', 'last_name', 'bio', 'phone', 'city', 'department', 'location', 'birth_date', 'country', 'organization', 'class_in', 'photo']
    

@login_required
def profile_picture(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST' and request.FILES['myfile']:
        profile = Edit_User.objects.get(user = user)
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
    return round((sum(x)/sum(i > 0 for i in x)), 1)

def get_or_create(tutor, name, scores):
    student_name = CNAME.objects.get(pk=name)
    instance = QSUBJECT.objects.filter(student_name__exact=student_name, tutor__exact = tutor)
    if not instance.exists():
        instance = QSUBJECT(student_name=student_name, tutor=tutor, test = scores[2], agn = scores[3], atd = scores[4], total = scores[5], exam = scores[6], agr = scores[7], grade = scores[8], posi = scores[9])
    else:
        instance = QSUBJECT.objects.get(student_name=student_name, tutor = tutor)
        if tutor.subject.name == 'BST 1' or tutor.subject.name == 'BST 2':
            if instance.tutor.model_in != '12' or instance.tutor.model_in != '21': 
                qr = QSUBJECT.objects.get(pk=instance.id)#loaded BST 1/BST 2
                qr.test, qr.agn, qr.atd, qr.total, qr.exam, qr.agr, qr.grade, qr.posi = average([qr.test, scores[2:][2]]), average([scores[2:][3] + qr.agn]), average([qr.atd, scores[2:][4]]), average([qr.total, scores[2:][5]]), average([qr.exam, scores[2:][6]]), average([qr.agr, scores[2:][7]]), do_grades(int([average([qr.agr, scores[2:][8]])]), cader(tutor.Class)), scores[2:][9]
                if tutor.model_in == 'qsubject':
                    tutor.model_in = tutor.subject.name[-1]
                else:
                    tutor.model_in = tutor.model_in + tutor.subject.name[-1]
                tutor.save()
        else:
            instance.test, instance.agn, instance.atd, instance.total, instance.exam, instance.agr, instance.grade, instance.posi = scores[2:]   
    instance.save()    
    return instance.student_id



def responsive_updates(request, pk):
    if pk == '0':#first and second terms       
        if request.GET.get('flow') == "toHtml":#feeding the html page
            tutor = BTUTOR.objects.get(pk=int(request.GET.get('tutor_id')))
            instance = QSUBJECT.objects.filter(tutor__exact = tutor).order_by('id')
            data = {"status":tutor.updated, "tutor_name":tutor.teacher_name}
            data["list"] = ['Default']+[[i.student_name.full_name, i.student_id, i.test, i.agn, i.atd, i.exam, i.grade, i.posi, i.student_name.gender, i.fagr, i.sagr, i.aagr, i.avr] for i in instance]

        if request.GET.get('flow') == "fromHtml":#fetching from the html page and save to the database.
            list = [request.GET.get('student_id'), request.GET.get('student_name'), request.GET.get('test'),request.GET.get('agn'),request.GET.get('atd'),request.GET.get('total'), request.GET.get('exam'),request.GET.get('agr'),request.GET.get('grade'),request.GET.get('posi')]
            tutor = BTUTOR.objects.get(pk=int(request.user.profile.account_id))
            data = {"status":"#oky_"+request.GET.get('sn'), 'count':str(len([i for i in list if i != None])), "id":str(get_or_create(tutor, int(request.GET.get('student_id').split("/")[-1]), list))}

        if request.GET.get('flow') == "confirm":
            if request.GET.get('Subject') == 'BST 1' or request.GET.get('Subject') == 'BST 2':
                Subject = 'BST'
            else:
                Subject = request.GET.get('Subject')
            exist = BTUTOR.objects.filter(accounts__exact = request.user, subject__name__exact = Subject, Class__exact = request.GET.get('Class'), term__exact = '1st Term')
            data = {"status":exist.exists()}
            if exist.exists(): 
                tutor = exist.first()
                if request.GET.get('Term') == '2nd Term' or request.GET.get('Term') == '3rd Term':
                    if request.GET.get('Term') == '2nd Term':
                        tutor.second_term = request.GET.get('Term')
                        tutors = TUTOR_HOME.objects.filter(first_term = exist.first()).first()
                        tutors.second_term = exist.first()
                    if request.GET.get('Term') == '3rd Term':
                        tutor.second_term = "2nd Term"
                        tutor.third_term = request.GET.get('Term')
                        tutors = TUTOR_HOME.objects.filter(first_term = exist.first()).first()
                        tutors.third_term = exist.first()
                    tutor.save()
                    tutors.save()
                user = Edit_User.objects.get(user = request.user)
                user.account_id = exist.first().id
                user.save()
                data = {"status":exist.exists(), 'updated':exist.first().updated, "tutor_name":exist.first().teacher_name, "tutor_id":exist.first().id}
        
        if request.GET.get('flow') == "registration":
              reged = CNAME(full_name = request.GET.get('last').upper() +' '+ request.GET.get('first').upper(), last_name = request.GET.get('last').upper(), middle_name = request.GET.get('middlename').upper(), first_name = request.GET.get('first').upper(), gender = int(request.GET.get('gender')), birth_date = request.GET.get('birth'), Class = request.GET.get('Class'))
              reged.save()
              student_id = reged.last_name[0] + reged.first_name[0]+'/'+request.GET.get('Class')[0]+'/'+session.profile.session[-2:]+'/'+str(reged.id)
              data = {"created":reged.created, "updated":reged.updated, "student_id":student_id}
        if request.GET.get('flow') == "create":
                exist = create_new_subject_teacher(request, request.GET.get('Subject'), request.GET.get('Class'), request.GET.get('Term'))
                user = Edit_User.objects.get(user = request.user)
                user.account_id = exist.id
                user.save()
                data = {"status":exist.id, "tutor_name":exist.teacher_name, "tutor_id":exist.id}
    elif pk == "1":
            names = QSUBJECT.objects.filter(tutor__Class__exact= request.GET.get('Class'), tutor__subject__name__exact= request.GET.get('Subject'), tutor__session__exact = session, tutor__term__exact = "1st Term").order_by('gender', 'student_name')
            data = {"status":str(names.count())}
            data["list"] = ['Default']+[[i.student_name.full_name, i.student_id] for i in names] 
            if names.count() == 0:
                names = CNAME.objects.filter(Class__exact= request.GET.get('Class'), session__exact = session.profile.session).order_by('gender', 'full_name')
                data = {"status":str(names.count())}
                data["list"] = ['Default']+[[i.full_name, i.last_name[0]+i.first_name[0]+'/'+i.Class[0]+'/'+i.session[-2:]+'/'+str(i.id)] for i in names]
    return JsonResponse(data)
