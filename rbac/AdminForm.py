from django import forms
from . import models

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PermissionAdminForm(forms.ModelForm):
    title=forms.CharField(
        widget=forms.TextInput(),

    )

    url=forms.CharField(

    )

    action=forms.ModelMultipleChoiceField(
        queryset=models.Action.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        initial=models.Action.objects.filter(code='GET'),
    )

    menu=forms.ModelChoiceField(
        queryset=models.Menu.objects.all(),
        required=False,
    )

    class Meta:
        model = models.Permission
        fields = ['title','url','action','menu']


class MessageAdminForm(forms.ModelForm):

    content_url=forms.URLField(
        label='输入跳转链接',
        required=False,
        widget=forms.URLInput(),
    )

    content_word=forms.CharField(
        label='输入文本内容',
        required=False,
        widget=CKEditorUploadingWidget(),
    )

    content = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model=models.Message
        fields='__all__'

    def __init__(self,*args,**kwargs):
        initial=kwargs.get('initial') or {}
        instance=kwargs.get('instance')
        if instance:
            if instance.is_jump:
                initial['content_url']=instance.content
            else:
                initial['content_word']=instance.content
        kwargs.update({'initial':initial,'instance':instance})
        super(MessageAdminForm, self).__init__(*args,**kwargs)


    def clean(self):

        is_jump=self.cleaned_data.get('is_jump')

        if is_jump:
            content_field_name='content_url'
        else:
            content_field_name='content_word'

        content=self.cleaned_data.get(content_field_name)

        if not content:
            self.add_error(content_field_name,'必填')
            return
        else:
            self.cleaned_data['content']=content
            return super(MessageAdminForm, self).clean()

    class Media:
        js=('js/message_editor.js',)


