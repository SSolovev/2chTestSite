from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _


class MyUserForm(UserCreationForm):
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "/./+/-/_ characters.")})
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(MyUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_('Duplicate email'))


class MessageForm(forms.Form):
    creator_name = forms.CharField(label=_(u'Your name'), max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    file  = forms.FileField(required=False)

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            file_type = file.content_type
            if file_type not in ('image/gif', 'image/jpeg'):
                raise forms.ValidationError(_('File type is not supported'))
        return file

    def clean_creator_name(self):
        return self.cleaned_data['creator_name']


class ThreadForm(forms.Form):
    creator_name = forms.CharField(label=_(u'Your name'), max_length=30)
    title = forms.CharField(label=_(u'Title'), max_length=30)
    description = forms.CharField(widget=forms.Textarea)
    file  = forms.FileField(required=False)

    def clean_file(self):
        file = self.cleaned_data['file']
        if file:
            file_type = file.content_type
            if file_type not in ('image/gif', 'image/jpeg'):
                raise forms.ValidationError(_('File type is not supported'))

        return file