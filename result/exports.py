# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 18:54:06 2019

@author: AdeolaOlalekan
"""
import os
from django.shortcuts import get_object_or_404#, redirect
import csv
from .models import QSUBJECT, BTUTOR, CNAME, REGISTERED_ID#, SESSION
import pandas as pd
from django.conf import settings
import requests
from bs4 import BeautifulSoup
from statistics import mean
from django.http import HttpResponse
from django.shortcuts import redirect
from result.flowerable import building
from result.imports import check_repeated_names
from result.utils import session
session = session()

module_dir = os.path.dirname(__file__)  # get current directory
file_path = os.path.join(module_dir, 'JSS 2.txt')
def sample_disply(request):
    #os.chdir(file_path)
    empty_list = open(file_path, "r" )
    return HttpResponse(empty_list, content_type='text/plain')

def sample_down(request):
    response = HttpResponse(content_type='text/plain')
    with open(file_path, 'r') as file:
        file_txt = file.read()
        contents = file_txt.split('\n');
        sd = [[x] for x in contents]
    writer = csv.writer(response)
    for each in sd:
        writer.writerow(each) 
    response['Content-Disposition'] ='attachment; filename="samples.txt"'
    return response 

def student_names(request, pk):
    if request.user.is_authenticated:
        Class = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3', 'BIO', 'ECO', 'CHE', 'ACC', 'ARB', 'GOV', 'ICT', 'PHY', 'LIT', 'COM', 'GEO', 'AGR', 'YOR', 'ELE', 'CTR', 'GRM'][int(pk)]
        file_path = os.path.join(settings.MEDIA_ROOT, 'student_names/'+Class+'.txt')
        response = HttpResponse(content_type='text/plain')
        with open(file_path, 'r') as file:
            file_txt = file.read()
            contents = file_txt.split('\n');
            if len([contents.index(n) for n in contents if len(n) < 2]) == 1:
                males = sorted([x[0].upper() for x in check_repeated_names([[x] for x in contents[:[contents.index(n) for n in contents if len(n) < 2][0]]])])
                females = sorted([x[0].upper() for x in check_repeated_names([[x] for x in contents[[contents.index(n) for n in contents if len(n) < 2][0]+1:]])])
            else:
                return redirect('home')
            sd = [[x] for x in males+['']+females]
        writer = csv.writer(response)
        for each in sd:
            writer.writerow(each)    
        response['Content-Disposition'] = "attachment; filename={Class}-names.txt".format(Class=Class)
        return response
    else:
        return redirect('home')

def export_name_text(request, pk, ty):#result download based on login tutor
    if int(pk) >= 1 and int(ty) != 0:
        tutor = get_object_or_404(BTUTOR, pk=pk)
        subject = QSUBJECT.objects.filter(tutor__exact=tutor).values_list('student_name')
        Class = tutor.Class
        # 
    else:
        Class = ['', 'JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'][int(pk)]
        subject = REGISTERED_ID.objects.filter(student_class__exact=Class, session__exact=session).values_list('student_name')
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = "attachment; filename={Class}-names.txt".format(Class=Class)
    writer = csv.writer(response)
    sd = [list(x) for x in subject]
    for i in range(0, len(sd)):
        sd[i][0] = CNAME.objects.get(pk=sd[i][0]).last_name+' '+ CNAME.objects.get(pk=sd[i][0]).first_name
    for each in sd:
        writer.writerow(each)
    return response  
#https://uqhs.herokuapp.com
def tutor(request):
    if request.user.profile.last_name != None and request.user.profile.first_name != None:
        return str(request.user.profile.last_name.upper())+'  '+str(request.user.profile.first_name.upper())
    else:
        return str(request.user.profile.last_name)+'  '+str(request.user.profile.first_name)


def scores(request, pk, ty):
    tutor = BTUTOR.objects.get(pk=pk)
    xr = [['table.qsubject', "table.annual"], [['name', 'test', 'agn', 'atd', 'tot', 'exam', 'agr', 'grd', 'pos'],['name', 't_test', 't_agn', 't_atd', 't_tot', 'exam', 't_agr', 's_agr', 'f_agr', 'annual', 'Agr', 'Grd', 'pos']], ['7', '8']]                 
    response = requests.get('https://uqhi.herokuapp.com/result/_all/'+str(pk)+'/'+xr[-1][['qsubject', 'annual'].index(tutor.model_in)]+'/')#url 
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.select_one(xr[0][['qsubject', 'annual'].index(tutor.model_in)])#tb
    headers = [th.get_text(",") for th in table.select("th")]
    headers[0] = tutor.teacher_name.upper()
    table_rows = soup.findAll('tr')
    lists = [[data.find(class_=x).get_text(',') for x in xr[1][['qsubject', 'annual'].index(tutor.model_in)]] for data in table_rows]
    if int(ty) == 1:
        df = pd.DataFrame(lists)
        df.index = [x+1 for x in range(len(df))]
        df.columns = headers
        df.to_csv(os.path.join(settings.MEDIA_ROOT, 'csvs/'+tutor.Class+'_'+tutor.subject.name+'_'+tutor.term+'_'+str(session)+'.csv'), encoding='ISO-8859-1')
        os.chdir(settings.MEDIA_ROOT)
        with open(os.path.join(settings.MEDIA_ROOT, 'csvs/'+tutor.Class+'_'+tutor.subject.name+'_'+tutor.term+'_'+str(session)+'.csv'), "r") as csvfile:
            data = list(csv.reader(csvfile)) 
            data[0][1] = 'STUDENT NAME'
        if tutor.model_in == 'annual':
                                                                                                                                               #[sum, avg, count, class, sheet]
            return building(request, [data, [sum([int(float(df.Avg[i+1])) for i in range(len(df))]), round(mean([int(float(df.Avg[i+1])) for i in range(len(df))]), 2), len(df), tutor.Class, tutor.term+' MarkSheet', headers, tutor.term+'/'+tutor.subject.name, tutor.teacher_name]])
        else:
            return building(request, [data, [sum([int(float(df.Sum[i+1])) for i in range(len(df))]), round(mean([int(float(df.Sum[i+1])) for i in range(len(df))]), 2), len(df), tutor.Class, tutor.term+' MarkSheet', headers, tutor.term+'/'+tutor.subject.name, tutor.teacher_name]])
    else:
        return export_csv_scores([tutor.Class, headers], lists)
    
 #https://uqhi.herokuapp.com   
def broadscores(request, pk, ty):
    classes = [['name', 'acc1', 'acc2', 'acc3', 'acc', 'ict1', 'ict2', 'ict3', 'ict', 'bio1', 'bio2', 'bio3', 'bio', 'agr', 'avr', 'grd', 'pos'], ['name', 'ent1', 'ent2', 'ent3', 'ent', 'mat1', 'mat2', 'mat3', 'mat', 'eng1', 'eng2', 'eng3', 'eng', 'agr', 'avr', 'grd', 'pos'], ['name', 'bus1', 'bus2', 'bus3', 'bus', 'yor1', 'yor2', 'yor3', 'yor',  'irs1', 'irs2', 'irs3', 'irs','agr', 'avr', 'grd', 'pos'], ['name', 'nva1', 'nva2', 'nva3', 'nva', 'non1', 'non2', 'non3', 'non', 'nil1', 'nil2', 'nil3', 'nil','agr', 'avr', 'grd', 'pos']]
    headers = [[['STUDENT NAME', '1st', '2nd', '3rd', 'Acc', '1st', '2nd', '3rd', 'Ict', '1st', '2nd', '3rd', 'Bio', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Ent', '1st', '2nd', '3rd', 'Mat', '1st', '2nd', '3rd', 'Eng', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Plc', '1st', '2nd', '3rd', 'Yor', '1st', '2nd', '3rd', 'Irs', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Civ', '1st', '2nd', '3rd', 'None', '1st', '2nd', '3rd', 'None', 'AGR', 'AVR', 'GRD', 'POS']], [['STUDENT NAME', '1st', '2nd', '3rd', 'Arb', '1st', '2nd', '3rd', 'His', '1st', '2nd', '3rd', 'Bst', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Prv', '1st', '2nd', '3rd', 'Mat', '1st', '2nd', '3rd', 'Eng', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Bus', '1st', '2nd', '3rd', 'Yor', '1st', '2nd', '3rd', 'Irs', 'AGR', 'AVR', 'GRD', 'POS'], ['STUDENT NAME', '1st', '2nd', '3rd', 'Nav', '1st', '2nd', '3rd', 'Agr', '1st', '2nd', '3rd', 'None', 'AGR', 'AVR', 'GRD', 'POS']]]
    response = requests.get('https://uqhi.herokuapp.com/result/create_update_annual_records/explorer/'+str(pk)+'/')
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.select_one("table.broadsheet")
    table_rows = soup.findAll('tr')
    lists = [[[data.find(class_=x).get_text(',') for x in classes[i]] for data in table_rows] for i in range(4)]
    dg = lists[0]+[headers[1][1]]+lists[1]+[headers[1][2]]+lists[2]+[headers[1][3]]+lists[3]
    if int(ty) == 1:
        df = pd.DataFrame(dg)
        sd = []
        for i in range(4):
            if i!=0:
                sd+=[None]
            sd = sd+[i+1 for i in range(len(lists[0]))]
        df.index = sd
        df.columns = headers[1][0]
        df.to_csv(os.path.join(settings.MEDIA_ROOT, 'csvs/'+request.user.profile.class_in+'_'+str(session)+'.csv'), encoding='ISO-8859-1')
        os.chdir(settings.MEDIA_ROOT)
        with open(os.path.join(settings.MEDIA_ROOT, 'csvs/'+request.user.profile.class_in+'_'+str(session)+'.csv'), "r") as csvfile:
            data = list(csv.reader(csvfile)) 
        return building(request, [data, [sum([int(float(x[-3])) for x in lists[0]]), round(mean([int(float(x[-3])) for x in lists[0]]), 2), len(lists[0]), request.user.profile.class_in, 'BROADSHEET', headers[1][0], 'BROADSHEET', tutor(request)]])
    else:
        return export_csv_scores([request.user.profile.class_in, headers[1][0]], dg)


def export_csv_scores(details, lists):#result download based on login tutor
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename={Class}.csv".format(Class=details[0])
    writer = csv.writer(response)
    writer.writerow(details[1])
    for each in lists:
        writer.writerow(each)
    return response 


def past_csvs(request, Class, subject, term, session, formats):
    os.chdir(settings.MEDIA_ROOT)
    xv = [['JSS 1', 'JSS 2', 'JSS 3', 'SSS 1', 'SSS 2', 'SSS 3'], ['ACC', 'AGR', 'ARB', 'BST', 'BIO', 'BUS', 'CTR', 'CHE', 'CIV', 'COM', 'ECO', 'ELE', 'ENG', 'FUR', 'GRM', 'GEO', 'GOV', 'HIS', 'ICT', 'IRS', 'LIT', 'MAT', 'NAV', 'PHY', 'PRV', 'YOR', None], ['1st Term', '2nd Term', '3rd Term', None]]
    if xv[1][int(subject)] != None and xv[2][int(term)] != None:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'csvs/'+str(xv[0][int(Class)])+'_'+str(xv[1][int(subject)])+'_'+str(xv[2][int(term)])+'_'+str(session)+'.csv')):
             xx = os.path.join(settings.MEDIA_ROOT, 'csvs/'+str(xv[0][int(Class)])+'_'+str(xv[1][int(subject)])+'_'+str(xv[2][int(term)])+'_'+str(session)+'.csv')
             df = pd.read_csv(xx, index_col = 0)
        else:
            return redirect('home')
    else:
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, 'csvs/'+str(xv[0][int(Class)])+'_'+str(session)+'.csv')):
            xx = os.path.join(settings.MEDIA_ROOT, 'csvs/'+str(xv[0][int(Class)])+'_'+str(session)+'.csv')
            df = pd.read_csv(xx, index_col = 0)
        else:
            return redirect('home')
    headers = df.columns
    if len(df) != 0:
        with open(xx, "r") as csvfile:
            data = list(csv.reader(csvfile))
            TUTOR_NAME = data[0][1]
            data[0][1] = 'STUDENT NAME'
        if int(formats) == 1:
            return export_csv_scores([str(xv[0][int(Class)]), headers[1][0]], data)
        else:
            if 'AVR' in df.columns:#broadsheets
                dim = [int(float(x)) for x in [df.iloc[0:int(df.iloc[-1:].index[0])].AVR[i+1] for i in range(len(df.iloc[0:int(df.iloc[-1:].index[0])]))] if x != 'None']                                                                                                                                   #[sum, avg, count, class, sheet]
                return building(request, [data, [sum(dim), round(mean(dim), 2), len(df.iloc[0:int(df.iloc[-1:].index[0])]), str(xv[0][int(Class)]), 'BROADSHEET', headers, 'BROADSHEET', tutor(request)]])
            elif 'Sum' in df.columns and xv[2][int(term)] != None and xv[1][int(subject)] != None:#1st and 2nd terms
                dim = [int(float(x)) for x in [df.Sum[i+1] for i in range(len(df))] if x != 'None']
                return building(request, [data, [sum(dim), round(mean(dim), 2), len(df), str(xv[0][int(Class)]), str(xv[2][int(term)])+' MarkSheet', headers, str(xv[2][int(term)])+'/'+str(xv[1][int(subject)]), TUTOR_NAME]])
            elif 'Avg' in df.columns and xv[2][int(term)] != None and xv[1][int(subject)] != None:#third terms
                dim = [int(float(x)) for x in [df.Avg[i+1] for i in range(len(df))] if x != 'None']
                return building(request, [data, [sum(dim), round(mean(dim), 2), len(df), str(xv[0][int(Class)]), str(xv[2][int(term)])+' MarkSheet', headers, str(xv[2][int(term)])+'/'+str(xv[1][int(subject)]), TUTOR_NAME]])
            else:
                return redirect('home')
    else:
        return redirect('home')

