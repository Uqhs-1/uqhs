from django.contrib.auth.models import User
from .models import QSUBJECT, CNAME, BTUTOR, Edit_User, ANNUAL, TUTOR_HOME
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin 
import os
from django.conf import settings
from result.utils import do_grades, do_positions, cader

class Teacher_model_view(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = BTUTOR
    fields = ['accounts', 'teacher_name', 'subject', 'Class', 'term', 'males', 'females', 'teacher_in', 'status']
    #success_url = reverse_lazy('home') 
    
    
class tutor_home_view(UpdateView):
    model = TUTOR_HOME
    fields = ['tutor', 'teacher_name', 'first_term', 'second_term', 'third_term']#, 'males', 'females', 'teacher_in', 'status']    

class Subject_model_view(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = QSUBJECT
    fields = ['student_name', 'test', 'agn', 'atd', 'total', 'exam', 'agr', 'grade', 'posi', 'tutor']


    
class Cname_edit(LoginRequiredMixin, UpdateView):#New teacher form for every new term, class, subjects
    model = CNAME
    fields = ['full_name', 'gender']
    
def manage_subject_updates(request, pk):
    tutor = BTUTOR.objects.get(pk=pk)
    ext = tutor.males+tutor.females - QSUBJECT.objects.select_related('tutor').filter(tutor__exact=tutor).count()
    QsubjectFormSet = modelformset_factory(QSUBJECT, exclude=('Class', 'logged_in', 'total', 'agr', 'grade', 'posi', 'gender', 'created', 'updated', 'cader', 'annual_scores',), extra=ext)
    if request.method == "POST":
        formset = QsubjectFormSet(request.POST, queryset=QSUBJECT.objects.select_related('tutor').filter(tutor__exact=tutor),)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    form.save()
            return redirect('many_subject_updates', pk=pk)
    else:
        formset = QsubjectFormSet(queryset=QSUBJECT.objects.select_related('tutor').filter(tutor__exact=tutor))
    return render(request, 'result/qsubject_formset.html', {'formset': formset, 'pk':pk, 'tutor' : tutor})

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

class Users_update(UpdateView):#New teacher form for every new term, class, subjects
    model = User
    fields = '__all__'
    success_url = reverse_lazy('all_accounts')


def many_student_updates(request, pk):#tutor
    query = QSUBJECT.objects.select_related('tutor').filter(tutor__exact=BTUTOR.objects.get(pk=pk))
    students = list(query.values_list('id'))
    ids = [r[0] for r in students]
    for i in range(0, query.count()):
        obj = QSUBJECT.objects.get(pk=ids[i])
        obj.total = obj.test + obj.agn + obj.atd
        obj.agr = obj.exam + obj.total
        obj.grade = do_grades([obj.agr], cader(obj.tutor.Class))[0]
        obj.save()
    return redirect('position_updates', pk=pk, term=3)


#@login_required
def single_student_update(request, pk):#student
    obj = QSUBJECT.objects.get(pk=pk)
    if obj.tutor != None:
        obj.total = obj.test + obj.agn + obj.atd
        obj.agr = obj.exam + obj.total
        obj.grade = do_grades([obj.agr], cader(obj.tutor.Class))[0]
        obj.save()
        return redirect('position_updates', pk=obj.tutor.id, term=3)
    else:
        return redirect('home')
@login_required
def subject_position_updates(request, pk, term):#all
    if int(term) == 4:
        query = ANNUAL.objects.select_related('subject_by').filter(subject_by__exact=BTUTOR.objects.get(pk=pk))
        students = [x[:] for x in list(query.values_list('Agr', 'id')) if x[0] != None]
    else:
        query = QSUBJECT.objects.select_related('tutor').filter(tutor__exact=BTUTOR.objects.get(pk=pk))
        students = [x[:] for x in list(query.values_list('agr', 'id')) if x[0] != None]
    agr = [r[0] for r in students]###############news
    posi = do_positions(agr[:])
    ids = [r[1] for r in students]
    if int(term) == 4:
        for i in range(0, len(agr)):
            objs = ANNUAL.objects.get(pk=ids[i])
            objs.grade = do_grades([int(objs.Agr)], cader(BTUTOR.objects.get(pk=pk).Class))[0]
            objs.Posi = posi[i]
            objs.save()
        return redirect('subject_view', pk=pk, md=2)
    else:
        for i in range(0, len(agr)):
            objs = QSUBJECT.objects.get(pk=ids[i])
            objs.posi = posi[i]
            objs.save()
        return redirect('subject_view', pk=pk, md=1)
        
