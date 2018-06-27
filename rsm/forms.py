from django import forms
from .models import profile, uploadFile
from django.contrib.auth.models import User


# 该文件用于描述并验证前端提交之后台的表单

# 用户使用的容器表单
class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['serverNum']


# 用户名，密码表单
class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


# 登录表单
class loginForm(forms.Form):
    username = forms.CharField(required=True, label=u'username', error_messages={'required': 'username is required'},
                               widget=forms.TextInput(attrs={'placeholder': u'username'}))
    password = forms.CharField(required=True, label=u'password', error_messages={'required': 'password is required'},
                               widget=forms.PasswordInput(attrs={'placeholder': u'password'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"username and password are required")
        else:
            cleaned_data = super(loginForm, self).clean()


# 上传文件表单
class uploadFileForm(forms.ModelForm):
    class Meta:
        model = uploadFile
        fields = ['file', 'targetContainer']


# 下载文件表单
class downloadFileForm(forms.Form):
    filename = forms.CharField(required=True, label='filename')


# 批量控制命令表单
class commandForm(forms.Form):
    command = forms.CharField(required=True, label='command')
