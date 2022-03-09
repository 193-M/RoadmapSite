from .forms import ClassEdit_Formset, ClassForm, Content_Formset, CustomUserCreationForm, ManagerCreationForm, UserEditForm, ManagerEditForm, LoginForm, RoadMapContentForm, RoadMapSelectForm, RoadMapTitleForm, RoadMapIndexForm, Index_FormSet, SelectClassForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, RoadMapContents, RoadMapTitles, UserClass
from django.urls import reverse
from urllib.parse import urlencode

def top(request):
    return render(request, 'top.html')

# ---- 利用者ビュー ----

# サインアップ
def usr_signupview(request): 
    form = CustomUserCreationForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email = email, password = password)
            login(request, user)
            return redirect('/mypage')
    return render(request, 'usr_signup.html', context)

# ログイン
def usr_loginview(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
    if request.method == 'POST':
        email = form.data['email']
        password = form.data['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            return redirect('usr_mypage')
        else:
            context = {'form':form, "error":"メールアドレスかパスワードが間違っています。"}
    return render(request, 'usr_login.html', context)

# マイページ
def usr_mypageview(request):
    return render(request, 'usr_mypage.html')

# 登録情報確認ページ
def usr_infoview(request): 
    return render(request, 'usr_info.html')

# 登録情報編集ページ
def usr_info_editview(request):
    form = UserEditForm(request.POST or None, instance=request.user)
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('usr_info')
    return render(request, 'usr_info_edit.html', context)

# ログアウト用ページ
def usr_logoutview(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login')
    return render(request, 'usr_logout.html')

# タスク確認ページ
def usr_taskview(request): 
    return render(request, 'usr_task.html')

# ロードマップ確認ページ
def usr_roadmapview(request):
    form = RoadMapSelectForm(request.POST or None)
    form.fields['select'].queryset = RoadMapTitles.objects.all()
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data['select']
            roadmap = RoadMapTitles.objects.get(title=title.title)
            contents = roadmap.roadmaptitle.all()
            data = True
            if len(contents) == 0:
                data = False
            context = {'contents':contents, 'form':form, 'title':roadmap.title, 'data':data}
    return render(request, 'usr_roadmap.html', context)

# ロードマップ確認詳細ページ
def usr_roadmap_indexview(request, content):
    contents = RoadMapContents.objects.get(content=content)
    select_content = contents.content
    indexes = contents.contenttitle.all()
    context = {'content':select_content, 'indexes':indexes}
    return render(request, 'usr_roadmap_index.html', context)

# ---- 管理者ビュー ----

# サインアップ
def mng_signupview(request):
    form = ManagerCreationForm(request.POST or None, initial={'is_staff':True})
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email = email, password = password)
            login(request, user)
            return redirect('mng_mypage')
    return render(request, 'mng_signup.html', context)

# ログイン
def mng_loginview(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
    if request.method == 'POST':
        email = form.data['email']
        password = form.data['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('mng_mypage')
            else:
                context = {'form':form, 'message': "ログイン権限がありません。"}
        else:
            context = {'form':form, 'message': "メールアドレスかパスワードが間違っています。"}
    return render(request, 'mng_login.html', context)

# マイページ
def mng_mypageview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    return render(request, 'mng_mypage.html')

# 登録情報確認ページ
def mng_infoview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    return render(request, 'mng_info.html')

# 登録情報編集ページ
def mng_info_editview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    form = ManagerEditForm(request.POST or None, instance=request.user)
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('mng_info')
    return render(request, 'mng_info_edit.html', context)

# ログアウトページ
def mng_logoutview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    if request.method == "POST":
        logout(request)
        return redirect('mng_login')
    return render(request, 'mng_logout.html')

# ロードマップ作成ページ タイトル
def mng_create_titleview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    form = RoadMapTitleForm(request.POST or None)
    context = {'form':form}
    if request.method == 'POST':
        if form.is_valid():
            new = form.save()
            return redirect('mng_create_content', title=new.title)
        else:
            context = {'form':form, 'message':"入力に不備があるか、既に同名のマップが存在します。"}
    return render(request, 'mng_create_title.html', context)

# redirect用url生成
def url_generate(url):
    parameter = {'change': "success"}
    query_string_parameter = urlencode(parameter)
    new_url = url + "?" + query_string_parameter
    return new_url

#ロードマップ作成ページ 内容
def mng_create_contentview(request, title):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    roadmap = RoadMapTitles.objects.get(title=title)
    contents = roadmap.roadmaptitle.all()
    form = RoadMapContentForm(request.POST or None, initial={'content_title':roadmap.pk})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('mng_create_content', kwargs={'title':title})
            new_url = url_generate(url)
            return redirect(new_url)
        else:
            context = {'form':form, 'title':title, 'contents':contents, 'error':"同じ名前のボックスが存在します。"}
    else:
        if 'change' in request.GET:
            context = {'form':form, 'title':title, 'contents':contents, 'success':"ボックスを追加しました"}
        else:
            context = {'form':form, 'title':title, 'contents':contents}
    return render(request, 'mng_create_content.html', context)

# ロードマップ作成ページ 詳細
def mng_create_indexview(request, title, content):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    contents = RoadMapContents.objects.get(content=content)
    select_content = contents.content
    indexes = contents.contenttitle.all()
    form = RoadMapIndexForm(request.POST or None, initial={'index_title':contents.pk})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            url = reverse('mng_create_index', kwargs={'title':title, 'content':content})
            new_url = url_generate(url)
            return redirect(new_url)
        else:
            context = {'form':form, 'title':title, 'content':select_content, 'indexes':indexes, 'error':"既に同様のボックスが存在します。"}
    else:
        if 'change' in request.GET:
            context = {'form':form, 'title':title, 'content':select_content, 'indexes':indexes, 'success':"ボックスを追加しました"}
        else:
            context = {'form':form, 'title':title, 'content':select_content, 'indexes':indexes}
    return render(request, 'mng_create_index.html', context)

# ロードマップ確認ページ
def mng_checkview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    form = RoadMapSelectForm(request.POST or None)
    form.fields['select'].queryset = RoadMapTitles.objects.all()
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            title = form.cleaned_data['select']
            roadmap = RoadMapTitles.objects.get(title=title.title)
            contents = roadmap.roadmaptitle.all()
            data = True
            if len(contents) == 0:
                data = False
            context = {'contents':contents, 'form':form, 'title':roadmap.title, 'data':data}
    return render(request, 'mng_check_roadmap.html', context)

# ロードマップ確認詳細ページ
def mng_check_indexview(request, content):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    contents = RoadMapContents.objects.get(content=content)
    roadmap = contents.content_title
    title = roadmap.title
    select_content = contents.content
    indexes = contents.contenttitle.all()
    data = True
    if len(indexes) == 0:
        data = False
    context = {'title':title, 'content':select_content, 'indexes':indexes, 'data':data}
    return render(request, 'mng_check_index.html', context)

# ロードマップ編集ページ
def mng_edit_contentview(request, title):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    roadmap = RoadMapTitles.objects.get(title=title)
    titleform = RoadMapTitleForm(request.POST or None, instance=roadmap)
    contents = roadmap.roadmaptitle.all()
    data = True
    if len(contents) == 0:
        data = False
    formset = Content_Formset(request.POST or None, queryset=contents)
    if request.method == "POST":
        if titleform.is_valid() and formset.is_valid():
            titleform.save()
            formset.save()
            url = reverse('mng_edit_content', kwargs={'title':title})
            new_url = url_generate(url)
            return redirect(new_url)
    else:
        if 'change' in request.GET:
            context = {'titleform':titleform, 'title':title, 'formset':formset, 'data':data, 'success':"変更を適用しました"}
        else:
            context = {'titleform':titleform, 'title':title, 'formset':formset, 'data':data}
    return render(request, 'mng_edit_content.html', context)

# ロードマップ編集詳細ページ
def mng_edit_indexview(request, title, content):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    select_content = RoadMapContents.objects.get(content=content)
    indexes = select_content.contenttitle.all()
    data = True
    if len(indexes) == 0:
        data = False
    formset = Index_FormSet(request.POST or None, queryset=indexes)
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            url = reverse('mng_edit_index', kwargs={'title':title, 'content':content})
            new_url = url_generate(url)
            return redirect(new_url)
        else:
            context = {'formset':formset, 'title':title, 'content':content, 'data':data}
    else:
        if 'change' in request.GET:
            context = {'title':title, 'content':content, 'formset':formset, 'data':data, 'success':"変更を適用しました"}
        else:
            context = {'formset':formset, 'title':title, 'content':content, 'data':data}
    return render(request, 'mng_edit_index.html', context)

# クラス一覧ページ
def mng_class_listview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    form = ClassForm(request.POST)
    class_list = UserClass.objects.all()
    context =  {'form':form, 'class_list':class_list}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('mng_class_list')
    return render(request, 'mng_class_list.html', context)

# ロードマップ削除ページ
def mng_delete_roadmapview(request, title):
    context = {'title':title}
    if request.method == 'POST':
        RoadMapTitles.objects.filter(title=title).delete()
        return redirect('mng_check')
    return render(request, 'mng_delete_roadmap.html', context)

# クラス編集ページ
def mng_class_editview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    formset = ClassEdit_Formset(request.POST or None, queryset=UserClass.objects.all())
    context = {'formset':formset}
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            redirect('mng_class_edit')
            context = {'formset':formset, 'message':"変更を適用しました"}
        else:
            context = {'formset':formset, 'message':"同名のクラスが存在します"}
    return render(request, 'mng_class_edit.html', context)

# 学生名簿ページ
def mng_studentsview(request):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    form = SelectClassForm(request.POST or None)
    context = {'form':form}
    if request.method == 'POST' and form.is_valid():
        select_class = form.cleaned_data['select_class']
        students = CustomUser.objects.filter(userclass=select_class)
        context = {'form':form, 'students':students}
    return render(request, 'mng_students.html', context)

# 学生詳細ページ
def mng_student_indexview(request, name):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    student = CustomUser.objects.get(username=name)
    context = {'student':student}
    return render(request, 'mng_student_index.html', context)

# 学生登録情報確認ページ
def mng_student_infoview(request, name):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    student = CustomUser.objects.get(username=name)
    context = {'student':student}
    return render(request, 'mng_student_info.html', context)

# 学生情報編集ページ
def mng_student_infoeditview(request, name):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    student = CustomUser.objects.get(username=name)
    form = UserEditForm(request.POST or None, instance=student)
    context = {'form':form, 'student':student}
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('mng_student_info', name)
    return render(request, 'mng_student_infoedit.html', context)

# 学生アカウント削除ページ
def mng_student_deleteview(request, name):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    context = {'name':name}
    if request.method == 'POST':
        CustomUser.objects.filter(name=name).delete()
        return redirect('mng_students')
    return render(request, 'mng_student_delete.html', context)

# 学生タスク確認ページ
def mng_student_taskview(request, name):
    if not request.user.is_staff:
        return redirect('usr_mypage')
    student = CustomUser.objects.get(username=name)
    context = {'student':student}
    return render(request, 'mng_student_task.html', context)