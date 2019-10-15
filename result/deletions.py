from .models import QSUBJECT, Post#, OVERALL_ANNUAL, TERM, SESSION
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required#, @permission_required

@login_required
def confirm_deleting_a_user(request, pk):
    qry = get_object_or_404(User, pk=pk)
    return render(request, 'result/confirm_delete_a_user.html', {'qry' : qry, 'pk': pk}) 
@login_required
def yes_no(request, pk):#delete single candidate
    qry = get_object_or_404(User, pk=pk)
    return render(request, 'result/yes_no.html', {'qry' : qry, 'pk': pk})
@login_required  
def delete_user(request, pk):#delete single candidate
    get_object_or_404(User, pk=pk).delete()
    return redirect('all_accounts')

@login_required
def confirm_deletion(request, pk):#sort for a deletion confirmation
    qry = get_object_or_404(QSUBJECT, pk=pk)
    return render(request, 'result/confirm_delete_a_student.html', {'qry' : qry, 'pk': pk})
@login_required
def confirmed_delete(request, pk):#Yes delete
    get_object_or_404(QSUBJECT, pk=pk).delete()
    return redirect('student_in_none')

@login_required
def delete_all(request):#Yes deletes
    QSUBJECT.objects.filter(tutor__accounts__exact=None, qteacher__exact=f'{request.user.profile.title}{request.user.profile.last_name} : {request.user.profile.first_name}').delete()
    return redirect('home')

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('my_post_list')