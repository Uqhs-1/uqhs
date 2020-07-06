from django.contrib.auth.models import User
from .models import QSUBJECT, CNAME, BTUTOR, Edit_User, ANNUAL, TUTOR_HOME, QUESTION, STUDENT_INFO, REGISTERED_ID
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
    fields = ['accounts', 'teacher_name', 'subject', 'Class', 'term', 'males', 'females', 'teacher_in', 'status', 'resumption']
    #success_url = reverse_lazy('home') 
    
    
class tutor_home_view(UpdateView):
    model = TUTOR_HOME
    fields = ['tutor', 'teacher_name', 'first_term', 'second_term', 'third_term']#, 'males', 'females', 'teacher_in', 'status']    

def Subject_model_view(request, pk):#New teacher form for every new term, class, subjects
    if request.method == 'POST':#
        data = [float(request.POST.get(i)) for i in ['test', 'agn', 'atd', 'exam']]
        qs = get_object_or_404(QSUBJECT, pk=pk)
        if qs.student_name != None:
            qs.test, qs.agn, qs.atd, qs.exam = data
            qs.tutor, qs.student_name = [get_object_or_404(BTUTOR, pk=int(request.POST.get('tutor'))), CNAME.objects.get(pk=int(request.POST.get('student_name')))]
            if request.POST.get('info') != 'None':
                qs.info = STUDENT_INFO.objects.get(pk=int(request.POST.get('info')))
            qs.save()
            return redirect('subject_updates', pk=pk)
        else:
            return redirect('subject_updates', pk=pk)
    else:
        model = QSUBJECT.objects.get(pk=pk)
    return render(request, 'result/qsubject_form.html', {'form': model, 'tutor':QSUBJECT.objects.select_related('tutor').filter(tutor__session__exact=model.tutor.session, tutor__Class__exact=model.tutor.Class, tutor__term__exact=model.tutor.term), 'info':STUDENT_INFO.objects.filter(Class=model.tutor.Class, session=model.tutor.session, term=model.tutor.term)})
    
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



@login_required
def subject_position_updates(request, pk, term):#all 
    from django.http import HttpResponse
    query = QSUBJECT.objects.select_related('tutor').filter(tutor__exact=BTUTOR.objects.get(pk=pk))
    students = [x for x in list(query.values_list('agr', 'id')) if x[0] != None]
    agr = [r[0] for r in students]###############news 
    posi = do_positions(agr)
    return HttpResponse(posi, content_type='text/plain')#
    grade = do_grades(agr, cader(BTUTOR.objects.get(pk=pk).Class))
    ids = [r[1] for r in students]
    for i in range(0, len(agr)):
        objs = QSUBJECT.objects.get(pk=ids[i])
        objs.posi = posi[i]
        objs.grade = grade[i]
        objs.save()
    return redirect('subject_view', pk=pk, md=1)

def average(x):
    return round((sum(x)/sum(i > 0 for i in x)), 1)

def get_or_create(tutor, name, scores):
    student_name = CNAME.objects.get(full_name=name)
    instance = QSUBJECT.objects.filter(student_name__exact=student_name, tutor__exact = tutor)
    if not instance.exists():
        instance = QSUBJECT(student_name=student_name, tutor=tutor, test = scores[1], agn = scores[2], atd = scores[3], total = scores[4], exam = scores[5], agr = scores[6], grade = scores[7], posi = scores[8])
    else:
        instance = QSUBJECT.objects.get(student_name=student_name, tutor = tutor)
        if tutor.subject.name == 'BST 1' or tutor.subject.name == 'BST 2':
            if instance.tutor.model_in == '12' or instance.tutor.model_in == '21': 
                qr = QSUBJECT.objects.get(pk=instance.id)#loaded BST 1/BST 2
                qr.test, qr.agn, qr.atd, qr.total, qr.exam, qr.agr, qr.grade, qr.posi = average([qr.test, scores[1:][1]]), average([scores[1:][2] + qr.agn]), average([qr.atd, scores[1:][3]]), average([qr.total, scores[1:][4]]), average([qr.exam, scores[1:][5]]), average([qr.agr, scores[1:][6]]), do_grades(average([qr.agr, scores[1:][7]]), cader(BTUTOR.objects.get(pk=instance.tutor.id).Class)), scores[1:][8]
                tutor.model_in == 'completed'
                tutor.save()
        else:
            instance.test, instance.agn, instance.atd, instance.total, instance.exam, instance.agr, instance.grade, instance.posi = scores[1:]
    if tutor.first_term == '1st Term':
        instance.fagr = scores[6]
    if tutor.second_term == '2nd Term':
        instance.sagr = scores[6]
    instance.save()    
    return instance.student_id

def responsive_updates(request, pk):
    if pk == '0':#first and second terms
        from .utils import session
        if request.GET.get('flow') == "toHtml":#feeding the html page
            tutor = BTUTOR.objects.get(pk=int(request.GET.get('tutor_id')))
            instance = QSUBJECT.objects.filter(tutor__exact = tutor).order_by('id')
            data = {"status":tutor.updated, "tutor_name":tutor.teacher_name}
            data["list"] = ['Default']+[[i.student_name.full_name, i.student_id, i.test, i.agn, i.atd, i.exam, i.grade, i.posi, i.student_name.gender, i.fagr, i.sagr, i.aagr, i.avr] for i in instance]

        if request.GET.get('flow') == "fromHtml":#fetching from the html page and save to the database.
            list = [request.GET.get('id'), request.GET.get('test'),request.GET.get('agn'),request.GET.get('atd'),request.GET.get('total'), request.GET.get('exam'),request.GET.get('agr'),request.GET.get('grade'),request.GET.get('posi')]
            tutor = BTUTOR.objects.get(pk=int(request.GET.get('tutor_id')))
            data = {"status":"#states_"+request.GET.get('sn'), 'count':str(len([i for i in list if i != None])), "id":str(get_or_create(tutor, request.GET.get('name'), list))}

        if request.GET.get('flow') == "confirm":
            if request.GET.get('Subject') == 'BST 1' or request.GET.get('Subject') == 'BST 2':
                Subject = 'BST'
            exist = BTUTOR.objects.filter(accounts__exact = request.user, subject__name__exact = Subject, Class__exact = request.GET.get('Class'), term__exact = '1st Term')
            data = {"status":exist.exists()}
            if exist.exists(): 
                if request.GET.get('Term') == '2nd Term':
                    exist.first().second_term = request.GET.get('Term')
                if request.GET.get('Term') == '3rd Term':
                    exist.first().third_term = request.GET.get('Term')
                data = {"status":exist.exists(), "tutor_name":exist.first().teacher_name, "tutor_id":exist.first().id}
        
        if request.GET.get('flow') == "registration":
                registered = REGISTERED_ID.objects.filter(student_name__full_name__exact=  request.GET.get('last') +' '+ request.GET.get('first'), student_class__exact=request.user.profile.class_in, session__exact=session)
                if not registered.exists():
                    name = CNAME.objects.filter(full_name_exact= request.GET.get('last') +' '+ request.GET.get('first'))
                    if not CNAME.objects.filter(full_name__exact
                     = request.GET.get('last') +' '+ request.GET.get('first')):
                        regs = CNAME(full_name = request.GET.get('last') +' '+ request.GET.get('first'), gender = request.GET.get('gender'), first_name = request.GET.get('first'), last_name = request.GET.get('last'))
                        regs.save()
                        new = REGISTERED_ID(student_name=regs,                  student_class=request.user.profile.class_in, session=session)     
                        new.save()
                        new.student_id = str(new.student_id)+'/'+ str(new.id)
                        new.save()    
                data = {"created":registered.first().created, "updated":registered.first().updated, "student_id":registered.first().student_id}
        if request.GET.get('flow') == "create":
                exist = create_new_subject_teacher(request, request.GET.get('Subject'), request.GET.get('Class'), request.GET.get('Term'))
                data = {"status":exist.id, "tutor_name":exist.teacher_name, "tutor_id":exist.id}
    elif pk == "1":
            names = QSUBJECT.objects.filter(tutor__Class__exact= request.GET.get('Class'), tutor__subject__name__exact= request.GET.get('Subject'), tutor__session__exact = 2024, tutor__term__exact = "1st Term")
            data = {"status":str(names.count())}
            data["list"] = ['Default']+[[i.student_name.full_name, i.student_id] for i in names]
    else:
        obj = get_object_or_404(ANNUAL, pk=pk)
        obj.anual = sum([float(request.GET.get('first')), float(request.GET.get('second')), float(request.GET.get('third'))])
        obj.Agr = round(mean([i for i in [float(request.GET.get('first')), float(request.GET.get('second')), float(request.GET.get('third'))] if i !=0]), 2)
        obj.save()
        data = {"status":str(obj.Agr)}
    return JsonResponse(data)