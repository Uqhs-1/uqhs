# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 20:05:17 2018

@author: AdeolaOlalekan
"""
import pandas as pd
from .models import QSUBJECT, CNAME, BTUTOR
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from result.result_views import cader
from django.contrib.auth.decorators import login_required
######################STAGE 2 ::: UPLOAD SCORES##################caders = ['jfo', 'sfo']
def bst_avg(dim):
    result = []
    for i in range(0, len(dim)):
        result += [[int(round((sum(dim[i][0:2])/sum(x > 0 for x in dim[i][0:2])+0.1), 0)), int(round((sum(dim[i][2:4])/sum(x > 0 for x in dim[i][2:4])+0.1), 0)), int(round((sum(dim[i][4:6])/sum(x > 0 for x in dim[i][4:6])+0.1), 0)), int(round((sum(dim[i][6:8])/sum(x > 0 for x in dim[i][6:8])+0.1), 0))]]
    return result 


@login_required
def test_file(request, pk):
    tutor = get_object_or_404(BTUTOR, pk=pk) 
    if request.method == "POST":
        my_file = request.FILES['files'] # get the uploaded file
        if not my_file.name.endswith('.txt'):
            messages.error(request,'File is not TXT type')
            return HttpResponseRedirect(reverse("upload_txt", pk=pk))
        #if file is too large, return
        if my_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (my_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("upload_txt", pk=pk))
        if my_file.content_type != 'text/plain':
            messages.error(request,'File content is not TXT type')
            return HttpResponseRedirect(reverse("upload_txt", pk=pk))
        file_txt = my_file.read().decode("ISO-8859-1")
        contents = file_txt.split('\n');
        new = [[], [], []]
        for line in contents:
            inn = [new.strip() for new in line.split(',')]
            new[0] += [inn]
        ind = [new[0].index(x) for x in new[0]]
        newx = [n[:] for n in new[0] if len(n) > 2]
        tutor.males = ind[-1]
        tutor.save()
        for i in range(0, len(newx)):
            new[1] += [[int(float(ints)) for ints in newx[i][1:]]]#[scores[1]
            new[2] += [newx[i][0]]# names[2]]
        if len(new[1][0]) == 8:#BST ONLY: Reduced 8 to 4 columns by averaging.
            x_y = bst_avg(new[1])
            new[1] = x_y
        sd = []
        for i in range(0, len(new[1])):
            sd += [[i+1]+new[1][i]+[sum(new[1][i][:3])]+[sum([new[1][i][3]+sum(new[1][i][:3])])]]
        dhead = pd.DataFrame(sd)
        for r in range(0, len(new[2])):
            cheack = CNAME.objects.filter(student_name=new[2][r], Class__exact=tutor.Class)#if name exits else create name
            if len(cheack) == 0:
                new_name = CNAME(student_name=new[2][r], Class=tutor.Class)#adding new student_name
                new_name.save()
        for i in range(0, len(dhead)):
            x = cader(tutor)
            MyModel = QSUBJECT(student_name=CNAME.objects.get(student_name=dhead.student_name[i]), test=dhead.test[i], agn=dhead.agn[i], atd=dhead.atd[i], exam=dhead.exam[i], total=dhead.total[i], agr=dhead.agr[i], gender=dhead.gender[i], posi=dhead.posi[i], logged_in=request.user, tutor = tutor, cader=x)
            MyModel.save() 
    else:#
        return render(request, 'result/loader.html', {'pk':pk, 'qry':tutor})
    return redirect('update_csv', pk=pk)

 
