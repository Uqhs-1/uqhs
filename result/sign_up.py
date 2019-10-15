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

