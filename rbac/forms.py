from django import forms

from rbac import models

class LoginForm(forms.Form):
    username=forms.CharField(
        label='账户名称',
        min_length=3,
        max_length=16,
        error_messages={'min_length': '最小长度3位','max_length': '最大长度16位'},
        widget=forms.TextInput(
            attrs={'class':'form-control'},
        ),
    )

    password=forms.CharField(
        label='账户密码',
        min_length=4,
        max_length=16,
        error_messages={'min_length': '最小长度4位', 'max_length': '最大长度16位'},
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'},
        ),
    )


    class Meta:
        models=models.User
        fields='__all__'