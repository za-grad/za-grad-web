from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'hide'
            }),
        }


class MassMailForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def send_mails(self):
        subject = self.cleaned_data.get('subject')
        body = self.cleaned_data.get('body')
        UserProfile.objects.send_notification_emails(
            UserProfile.objects.notification_emails, subject, body,
            include_greeting=True)
