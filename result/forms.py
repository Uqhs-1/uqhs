

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 08:25:37 2019

@author: AdeolaOlalekan
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BTUTOR, CNAME, ASUBJECTS, Edit_User, QSUBJECT, Post, SESSION, DOWNLOADFORMAT


class subjectforms(forms.ModelForm):
    class Meta:
        model = ASUBJECTS
        fields = ( 'name',)
            
class login_form(forms.Form):
    username = forms.CharField(max_length=18)#, help_text="Just type 'renew'")
    password1 = forms.CharField(widget=forms.PasswordInput)#
    
    def clean_data(self):
        data = self.cleaned_data['username']
        data = self.cleaned_data['password1']
        return data


###############################################################################  


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Edit_User
        fields = ('title', 'first_name', 'last_name', 'bio', 'phone', 'city', 'country', 'organization', 'location', 'birth_date', 'department', 'photo',)
        exclude = ['user']
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required for a valid signup!')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user
        
class subject_class_term_Form(forms.ModelForm):
    class Meta:
        model = BTUTOR
        fields = ('Class', 'term', )
        
class sessions(forms.ModelForm):
    class Meta:
        model = SESSION
        fields = ('new',)
        

class FORMARTS(forms.ModelForm):
    class Meta:
        model = DOWNLOADFORMAT
        fields = ('formats',)
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('Account_Username', 'subject', 'text') 
        
class a_student_form_new(forms.ModelForm):
    class Meta:
        model = QSUBJECT
        fields = ('student_name','test', 'agn','atd', 'exam','tutor', 'Class',)
        

class student_name(forms.ModelForm):
    class Meta:
        model = CNAME
        fields = ('last_name', 'first_name', 'gender',)

class new_student_name(forms.Form):
    student_name = forms.CharField(help_text="enter student's surename to search.")
    def clean_renewal_date(self):
        data = self.cleaned_data['student_name']
        return data
    
#