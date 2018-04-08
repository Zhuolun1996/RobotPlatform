from django import forms
from .models import profile, uploadFile
from django.contrib.auth.models import User


class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['serverNum']


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


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


class uploadFileForm(forms.ModelForm):
    class Meta:
        model = uploadFile
        fields = ('file','targetContainer')

class downloadFileForm(forms.ModelForm):
    filename=forms.CharField(required=True,label='filename')