from django.conf.urls import url
from.import views, imports, loggins, posts, sign_up, creates, deletions, updates
urlpatterns = [
            #####EXPORTS #######IMPORTS#####          
            url('home_page/(?P<pk>\d+)/$', views.home_page, name='home_page'),
            url(r'home/$', views.home, name='home'),
            url(r'offline/(?P<pk>\d+)/$', views.offline, name='offline'),
            url(r'home_page_return/(?P<pk>\d+)/$', views.home_page_return, name='home_page_return'),
            url('samples_down/', views.sample_down, name='samples_down'),
            url('samples_disp/', views.sample_disply, name='samples_disp'),
            url(r'^upload_txt/(?P<pk>\d+)/', imports.upload_new_subject_scores, name='upload_txt'),
            url('setup_questions/', imports.setup_questions, name='setup_questions'),
            url('pdf_compressor/(?P<pk>\d+)/$', views.pdf_compressor, name='pdf_compressor'),
            url('signup/', sign_up.Staff_SignUp.as_view(), name='signup'),
            url('user_qury/', sign_up.user_qury, name='user_qury'),
         			 #####VIEWS#####  
            url(r'searchs', views.searchs, name='searchs'),
            url(r'card_comments', views.card_comment, name='card_comments'),
            url(r'student_info/(?P<pk>\d+)/', views.student_info, name='student_info'),
            url(r'student_info_json/', views.student_info_json, name='student_info_json'),
            url(r'student_login/', views.student_home_page, name='student_login'),
            url('subject_home/(?P<pk>\d+)/(?P<cl>\d+)/', views.subject_home, name='subject_home'),
            url('render/pdf/(?P<pk>\d+)/(?P<ty>\d+)/(?P<sx>\d+)/', views.Pdf.as_view(), name='pdf'),
            url('url/pdf/url/(?P<pk>\d+)/', views.call_url, name='call_url'), 
            url('do_a_write/pdf/url/(?P<pk>\d+)/', views.do_a_write, name='do_a_write'),
             
            url('student_exam_page/(?P<pk>\d+)/(?P<SUB>[\w\-]+)/', views.student_exam_page, name='student_exam_page'), 
            url(r'^(?P<pk>\d+)/(?P<md>\d+)/', views.detailView, name='subject_view'),######################
            url(r'^_all/(?P<pk>\d+)/(?P<md>\d+)/', views.all_View, name='subject_view_all'),####################
            url('quest_filter/(?P<tm>\d+)/(?P<cl>\d+)/(?P<sj>[\w\-]+)/', views.quest_filter, name='quest_filter'),
            url('student_names/(?P<pk>\d+)/', views.Student_names_list, name='student_names'),
            url('student_on_all_subjects_list/(?P<pk>\d+)/', views.student_on_all_subjects_list, name='student_on_all_subjects_list'),
            url('all_student_subject_list/(?P<pk>\d+)/', views.all_student_subject_list, name='all_student_subject_list'),
            url('student_subject_list/(?P<pk>\d+)/', views.student_subject_list, name='student_subject_list'),
            url('all_teachers/', views.all_teachers, name='all_teachers'),#annual_sheet
            url(r'^subject/transfers', views.teacher_accounts, name='transfers'),
            url('editQuest/(?P<pk>\d+)/', views.editQuest, name='editQuest'),
            url(r'^results_junior_senior/(?P<pk>\d+)/', views.results_junior_senior, name='results_junior_senior'),
            url(r'^once_results_junior_senior/(?P<pk>\d+)/', views.once_results_junior_senior, name='once_results_junior_senior'),
            url(r'^student_subject_detail_one_subject/(?P<pk>\d+)/', views.student_subject_detail_one_subject, name='student_subject_detail_one_subject'),
            url(r'^genders_scores/(?P<pk_code>[\w\-]+)/', views.genders_scores, name='males_scores'),
            url('search_results/(?P<pk>\d+)/', views.search_results, name='search_results'),
            			 #####CREATES##### ques_subject_updates 
            
            url(r'search_pdf/', creates.search_pdf, name='search_pdf'),
            url(r'create_new_teacher/', creates.create_new_subject_teacher, name='teacher_create'),
            url(r'logins/', loggins.loggin, name='logins'),
            url('log_out/', loggins.logout, name='log_out'),
            url('admin_page/', loggins.admin_page, name='admin_page'),
            url('passwords/(?P<pk>\d+)/', loggins.password1, name='passwords'),
            url('password/', loggins.password2, name='password'),
            url('InputTypeError/', loggins.InputTypeError, name='InputTypeError'),
            url('all_accounts/', loggins.all_users, name='all_accounts'),
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
            url('yes_no/ deletions/ (?P<pk>\d+)/', deletions.yes_no, name='yes_no'),
            url('warning_delete/ deletions/ (?P<pk>\d+)/', deletions.delete_all, name='warning_delete'),
            url(r'^deletes/ deletions/', deletions.delete_all, name='deletes'), 
            url('confirm_deleting_a_user/ deletions/ (?P<pk>\d+)/', deletions.confirm_deleting_a_user, name='confirm_deleting_a_user'),
            url('delete_a_user/ deletions/ (?P<pk>\d+)/', deletions.delete_user, name='delete_a_user'),
            url('post_remove/ deletions/ (?P<pk>\d+)/', deletions.delete_post, name='post_remove'),
            			 #####UPDATES%###### 
            url('edit_accounts/ updates/ (?P<pk>\d+)/', updates.Users_update.as_view(), name='edit_accounts'),
            url('tutor/updates/(?P<pk>\d+)/', updates.Teacher_model_view.as_view(), name='tutor_update'),
            url('responsive_updates/(?P<pk>\d+)/', updates.responsive_updates, name='responsive_updates'),
            url('tutor/updates/home/(?P<pk>\d+)/', updates.tutor_home_view.as_view(), name='tutor_home_view'),
            url('subject_updates_model/updates/(?P<pk>\d+)/', updates.Subject_model_view, name='subject_updates_model'),
            url('question_image/(?P<pk>\d+)/', updates.question_image, name='question_image'),
            
            url('pro_detail/updates/(?P<pk>\d+)/', updates.profiles, name='pro_detail'),####
            url('user/updates/(?P<pk>\d+)/$', updates.ProfileUpdate.as_view(), name='user_update'),#####
            url('upload_photo/ updates/ (?P<pk>\d+)/', updates.profile_picture, name='upload_photo'),#####
            url(r'^Cname_edit/updates/(?P<pk>\d+)/$', updates.Cname_edit.as_view(), name='Cname_edit'),####
            url('position_updates/updates/(?P<pk>\w+)/(?P<term>\d+)/$', updates.subject_position_updates, name='position_updates'),
            
               
            url('', loggins.flexbox, name='flexing'),
                    
				]