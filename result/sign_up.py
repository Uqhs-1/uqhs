# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 05:10:08 2019

@author: AdeolaOlalekan
"""
from .forms import SignUpForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
class Staff_SignUp(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('registration:logins')
    form_valid_message = 'User has been created successfully!'
    form_invalid_message = 'Something wrong'
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                fd = form.cleaned_data
                username = fd['username']
                email = fd['email']
                password1 = fd['password1']
                password2 = fd['password2']
                password = None
                if password1 == password2:
                    password = password1
                if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                    userObj = User.objects.create_user(username=username, email=email, password=password)
                    userObj.is_active = False
                    userObj.email = fd['email']
                    userObj.save()
                    profile = userObj.profile
                    #profile.account = ['', 'Student', 'Staff']
                    profile.save()
                    return render(request, 'registration/account_activation_sent.html')
                else:
                    return HttpResponse("This Email Already exists, Use another email address please!")
    
        else:
            form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

    

###############################################################################
from django.http import JsonResponse
from .models import QSUBJECT
from django.shortcuts import redirect
def user_qury(request):
    if request.GET.get('username', None) != None:
        if User.objects.filter(username__iexact=request.GET.get('username', None)).exists() == True:
            data = {'is_taken': User.objects.filter(username__iexact=request.GET.get('username', None)).exists()}
            if data['is_taken']:
                data['error_message'] = 'A user with this username already exists.'
        else:
            data = {'is_taken': 'null'}
            data['error_message'] = 'Username does not exist.' 
        query = User.objects.all()
        for i in range(query.count()):
            data[query[i].username] = query[i].email
    else:
        if request.POST.get('username', None) != None:
                userObj = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
                userObj.is_active = True
                userObj.save()
                profile = userObj.profile
                profile.save()
                return redirect('home')
        else:
            if request.GET.get('student_id', None) != None:
                aunty = QSUBJECT.objects.filter(student_id__iexact=request.GET.get('student_id'))
                if aunty:
                      data = {'valid_id': aunty.exists(), 'name': aunty.first().student_name.full_name}
                data['error_message'] = 'The student ID entered is either not correct or does not exists.'
    return JsonResponse(data)
    
