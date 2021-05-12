from django.conf.urls import url
from.import views, imports, posts, sign_up_or_log_in, creates, deletions, updates
urlpatterns = [
            #####EXPORTS #######IMPORTS#####  
            url(r'home/$', views.home, name='home'),
            url(r'offline/(?P<pk>\d+)/$', views.offline, name='offline'),
            url(r'massRegistration/', imports.massRegistration, name='massRegistration'),
            url('samples_down/', views.sample_down, name='samples_down'),
            url('name_down/(?P<pk>\d+)/(?P<fm>\d+)/(?P<ps>\d+)/', views.name_down, name='name_down'),
            url('samples_disp/', views.sample_disply, name='samples_disp'),
            url(r'^upload_txt/', imports.upload_new_subject_scores, name='upload_txt'),
            url('setup_questions/', imports.setup_questions, name='setup_questions'),            
            url('user_qury/', sign_up_or_log_in.user_qury, name='user_qury'),
         			 #####VIEWS##### 
            url('all_users/(?P<pk>\d+)/', views.all_users, name='all_users'),           
            #url('templatesPdf/', views.lesson_templates.as_view(), name='templatesPdf'),
            url(r'searchs', views.searchs, name='searchs'),
            url(r'card_comments', views.card_comment, name='card_comments'),
            url(r'student_info/(?P<pk>\d+)/', views.student_info, name='student_info'),
            url(r'student_info_json/', views.student_info_json, name='student_info_json'),
            url(r'student_exam_page/(?P<subj_code>\d+)/(?P<pk>\d+)/', views.student_exam_page, name='student_exam_page'),
            url(r'accid/(?P<pk>\d+)/(?P<md>\d+)/', views.accid, name='accid'),
            url('subject_home/(?P<pk>\d+)/(?P<cl>\d+)/', views.subject_home, name='subject_home'),
            url('render/pdf/(?P<ty>\d+)/(?P<sx>\d+)/(?P<pk>\d+)/', views.Pdf.as_view(), name='pdf'),
            url(r'uniqueness/(?P<pk>\d+)/', views.uniqueness, name='uniqueness'),
            url('student_home_page/(?P<pk>\d+)/', views.student_home_page, name='student_home_page'), 
            url(r'^(?P<pk>\d+)/(?P<md>\d+)/', views.detailView, name='subject_view'),###################### 
            url(r'^_all/(?P<pk>\d+)/(?P<md>\d+)/', views.all_View, name='subject_view_all'),#################### student_subject_list
            #url('quest_filter/(?P<tm>\d+)/(?P<cl>\d+)/(?P<sj>[\w\-]+)/', views.quest_filter, name='quest_filter'),
            url('student_names/(?P<pk>\d+)/', views.Student_names_list, name='student_names'),
            #results_junior_senior#annual_sheet
            url(r'^subject/transfers/(?P<md>\d+)/', views.teacher_accounts, name='transfers'),
            url(r'^auto_pdf_a/transfers/(?P<md>\d+)/', views.auto_pdf_a, name='auto_pdf_a'),
            url('editQuest/(?P<pk>\d+)/', views.editQuest, name='editQuest'),
            url(r'^results_junior_senior/(?P<pk>\d+)/', views.results_junior_senior, name='results_junior_senior'),
            url('search_results/(?P<pk>\d+)/', views.search_results, name='search_results'),
            			 #####CREATES##### ques_subject_updates  
            
            
            url(r'create_new_teacher/', creates.create_new_subject_teacher, name='teacher_create'),
            url(r'logins/', sign_up_or_log_in.loggin, name='logins'),
            url('log_out/', sign_up_or_log_in.logout, name='log_out'),
            url('admin_page/', sign_up_or_log_in.admin_page, name='admin_page'),
            url('passwords/(?P<pk>\d+)/', sign_up_or_log_in.password1, name='passwords'),
            url('password/', sign_up_or_log_in.password2, name='password'),
            url('InputTypeError/', sign_up_or_log_in.InputTypeError, name='InputTypeError'),
            url('all_accounts/', sign_up_or_log_in.all_users, name='all_accounts'),
              #####POSTS%###### search_tutors
            url('my_post/post_list', posts.my_post, name='my_post_list'),
            url('post/post_list', posts.post_list, name='post_list'),
            url('post/(?P<pk>\d+)/', posts.post_detail, name='post_detail'),
            url('post/new/', posts.post_new, name='post_new'),
            url('post_edit/(?P<pk>\d+)/', posts.post_edit.as_view(), name='post_edit'),
            url('drafts/', posts.post_draft_list, name='post_draft_list'),#post approvals student_in_none new_student_name
            
            url('posts_publishing/(?P<pk>\d+)/publish/', posts.posts_publishing, name='posts_publishing'),
              ####DELETE%######  
            url('delete_warning/ deletions/ (?P<pk>\d+)/', deletions.confirm_deletion, name='delete_warning'),
            url(r'^delete_a_student/ deletions/ (?P<pk>\d+)/', deletions.confirmed_delete, name='delete'),
            url(r'^deletions/', deletions.deletes, name='deletes'),
            url('yes_no/ deletions/ (?P<pk>\d+)/', deletions.yes_no, name='yes_no'),
            url('warning_delete/ deletions/(?P<pk>\d+)/', deletions.warning_delete, name='warning_delete'),
            url(r'^deletes/ deletions/(?P<pk>\d+)/', deletions.delete, name='confirmed'), 
            url('confirm_deleting_a_user/ deletions/ (?P<pk>\d+)/', deletions.confirm_deleting_a_user, name='confirm_deleting_a_user'),
            url(r'^deletes/ deletions/(?P<pk>\d+)/', deletions.delete, name='confirmed'),
            url('delete_a_user/ deletions/ (?P<pk>\d+)/', deletions.delete_user, name='delete_a_user'),
            url('post_remove/ deletions/ (?P<pk>\d+)/', deletions.delete_post, name='post_remove'),
            			 #####UPDATES%###### 
            url('edit_accounts/ updates/ (?P<pk>\d+)/', updates.Users_update.as_view(), name='edit_accounts'),
            url('create_local_accounts/updates/(?P<x>\d+)/', updates.create_local_accounts, name='create_local_accounts'),
            url('tutor/updates/(?P<pk>\d+)/', updates.Teacher_model_view, name='tutor_update'),
            url('responsive_updates/(?P<pk>\d+)/', updates.responsive_updates, name='responsive_updates'),
            #
            url('need_tutor', updates.need_tutor, name='need_tutor'),
            url('question_image/(?P<pk>\d+)/', updates.question_image, name='question_image'),
            
            url('synchronizing/(?P<last>\d+)/(?P<subject>\d+)/(?P<Class>\d+)/$', updates.synch, name='synch'),
            url('pro_detail/updates/(?P<pk>\d+)/', updates.profiles, name='pro_detail'),####
            url('user/updates/(?P<pk>\d+)/$', updates.ProfileUpdate.as_view(), name='user_update'),#####
            url('upload_photo/ updates/ (?P<pk>\d+)/', updates.profile_picture, name='upload_photo'),#####
            url(r'^Cname_edit/updates/(?P<pk>\d+)/$', updates.Cname_edit.as_view(), name='Cname_edit'),####
            
               
            url('', sign_up_or_log_in.flexbox, name='flexing'),
                    
				]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
