from django import forms
from django.core.exceptions import ValidationError
from rbac import models

class LoginForm(forms.Form):
    username=forms.CharField(
        label='账户名称',
        min_length=2,
        max_length=16,
        error_messages={'min_length': '最小长度2位','max_length': '最大长度16位'},
        widget=forms.TextInput(
            attrs={'class':'form-control'},
        ),
    )

    password=forms.CharField(
        label='账户密码',
        min_length=6,
        max_length=16,
        error_messages={'min_length': '最小长度6位', 'max_length': '最大长度16位'},
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
        ),
    )

    class Meta:
        models=models.User
        fields='__all__'


class ChangePWDForm(forms.Form):
    username=forms.CharField(
        label='账户名称',
        widget=forms.TextInput(
            attrs={'class': 'form-control','readonly':'readonly','title':'用户名不可更改'}
        )
    )

    password1 = forms.RegexField(
        regex='^(?=.*[0-9])(?=.*[a-zA-Z])[0-9a-zA-Z]{6,16}$',
        min_length=6,
        max_length=16,
        label='新密码',
        error_messages={
            'min_length': '最小长度6位',
            'max_length': '最大长度16位',
            'invalid': '密码必须包含数字，字母',
        },
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
        ),
    )

    password2 = forms.CharField(
        label='确认新密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
        ),
    )

    def clean(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 == pwd2:
            return self.cleaned_data
        else:
            self.add_error('password1',ValidationError('密码不一致！'))
            return self.cleaned_data