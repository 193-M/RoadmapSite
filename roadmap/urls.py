from django.urls import path
from .views import top, usr_mypageview, usr_loginview, usr_roadmap_indexview, usr_signupview, usr_infoview, usr_info_editview, usr_roadmapview, usr_taskview, usr_logoutview
from .views import mng_mypageview, mng_signupview, mng_loginview, mng_infoview, mng_info_editview, mng_logoutview, mng_create_titleview, mng_create_contentview, mng_create_indexview, mng_checkview, mng_check_indexview, mng_edit_contentview, mng_edit_indexview, mng_class_listview, mng_class_editview, mng_studentsview, mng_student_indexview, mng_student_taskview, mng_student_infoview

urlpatterns = [
    path('', top),
    # 利用者パス
    path('login/', usr_loginview, name = 'usr_login'),
    path('signup/', usr_signupview, name = 'usr_signup'),
    path('mypage/', usr_mypageview, name = 'usr_mypage'),
    path('mypage/roadmap/', usr_roadmapview, name = 'usr_roadmap'),
    path('mypage/roadmap/<str:content>', usr_roadmap_indexview, name = 'usr_roadmap_index'),
    path('mypage/task/', usr_taskview, name = 'usr_task'),
    path('mypage/info/', usr_infoview, name = 'usr_info'),
    path('mypage/info/edit', usr_info_editview, name = 'usr_info_edit'),
    path('logout/', usr_logoutview, name = 'usr_logout'),
    # 管理者パス
    path('manage/login/', mng_loginview, name = 'mng_login'),
    path('manage/signup/', mng_signupview, name = 'mng_signup'),
    path('manage/mypage/', mng_mypageview, name = 'mng_mypage'),
    path('manage/mypage/info/', mng_infoview, name = 'mng_info'),
    path('manage/mypage/info/edit', mng_info_editview, name = 'mng_info_edit'),
    path('manage/logout/', mng_logoutview, name = 'mng_logout'),
    path('manage/create/', mng_create_titleview, name = 'mng_create_title'),
    path('manage/create/<str:title>/', mng_create_contentview, name = 'mng_create_content'),
    path('manage/create/<str:title>/<str:content>', mng_create_indexview, name = 'mng_create_index'),
    path('manage/check/', mng_checkview, name = 'mng_check'),
    path('manage/check/<str:content>', mng_check_indexview, name = 'mng_check_index'),
    path('manage/edit/<str:title>', mng_edit_contentview, name = 'mng_edit_content'),
    path('manage/edit/<str:title>/<str:content>', mng_edit_indexview, name = 'mng_edit_index'),
    path('manage/class/', mng_class_listview, name = 'mng_class_list'),
    path('manage/class/edit', mng_class_editview, name = 'mng_class_edit'),
    path('manage/students/', mng_studentsview, name = 'mng_students'),
    path('manage/students/<str:name>/', mng_student_indexview, name = 'mng_student_index'),
    path('manage/students/<str:name>/info/', mng_student_infoview, name = 'mng_student_info'),
    path('manage/students/<str:name>/task/', mng_student_taskview, name = 'mng_student_task'),
]