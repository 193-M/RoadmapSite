from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, RoadMapIndexes, RoadMapTitles, RoadMapContents, UserClass
from django.contrib.auth import password_validation

# セレクトボックス表示変更
class CustomClassChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.userclass

# 利用者用サインアップフォーム
class CustomUserCreationForm(UserCreationForm):
    userclass = CustomClassChoiceField(UserClass.objects.all(), label="クラス")
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'userclass')
        labels = {
            'username': "名前",
            'email': "メールアドレス",
            'userclass': "クラス"
        }

# 管理者用サインアップフォーム
class ManagerCreationForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff')
        labels = {
            'username': "名前",
            'email': "メールアドレス",
            'is_staff': "スタッフ権限"
        }
        widgets = {
            'is_staff':forms.HiddenInput
        }

# ログインフォーム
class LoginForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス', 
        max_length=255,
    )
    password = forms.CharField(
        label=("パスワード"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

# 管理者情報編集フォーム
class ManagerEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = {'username', 'email'}
        labels ={'username':"名前", 'email':"メールアドレス"}

# 利用者情報編集フォーム
class UserEditForm(forms.ModelForm):
    userclass = CustomClassChoiceField(UserClass.objects.all(), label="クラス")
    class Meta:
        model = CustomUser
        fields = {'username', 'email', 'userclass'}
        labels ={'username':"名前", 'email':"メールアドレス", 'userclass':"クラス"}

# クラス設定フォーム
class ClassForm(forms.ModelForm):
    class Meta:
        model = UserClass
        fields = '__all__'
        labels = {'userclass':"クラス"}

# クラス選択フォーム
class SelectClassForm(forms.ModelForm):
    select_class = CustomClassChoiceField(
        UserClass.objects,
        label="表示するクラス",
        empty_label="選択してください",
        to_field_name='userclass'
    )
    class Meta:
        model = UserClass
        fields = ('select_class',)

# ロードマップタイトルフォーム(大項目)
class RoadMapTitleForm(forms.ModelForm):
    class Meta:
        model = RoadMapTitles
        fields = '__all__'
        labels = {'title': "タイトル"}

# ロードマップ内容フォーム(中項目)
class RoadMapContentForm(forms.ModelForm):
    class Meta:
        model = RoadMapContents
        fields = ('content', 'content_title')
        widgets = {'content_title':forms.HiddenInput}
    
# ロードマップ詳細フォーム(小項目)
class RoadMapIndexForm(forms.ModelForm):
    class Meta:
        model = RoadMapIndexes
        fields = '__all__'
        widgets = {'index_title':forms.HiddenInput}

# セレクトボックス表示変更
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title

# ロードマップ選択フォーム
class RoadMapSelectForm(forms.ModelForm):
    select = CustomModelChoiceField(
        queryset=RoadMapTitles.objects,
        label="表示するロードマップ",
        empty_label="選択してください",
        to_field_name='title'
    )
    class Meta:
        model = RoadMapTitles
        fields = ('select',)

# ロードマップ編集用フォームセット
Content_Formset = forms.modelformset_factory(
    RoadMapContents,
    form=RoadMapContentForm,
    extra=0,
    can_delete=True
)

Index_FormSet = forms.modelformset_factory(
    RoadMapIndexes,
    form=RoadMapIndexForm,
    extra=0,
    can_delete=True
)

# クラス編集用フォームセット
ClassEdit_Formset = forms.modelformset_factory(
    UserClass,
    form=ClassForm,
    extra=0,
    can_delete=True
)