from django import forms
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Membership


class ContactForm(forms.Form):
    from_email = forms.EmailField(label='tvoja email adresa')
    subject = forms.CharField(label='naslov')
    body = forms.CharField(widget=forms.Textarea, label='poruka')

    def send(self):
        cd = self.cleaned_data
        from_email = cd.get('from_email')
        msg = EmailMessage(
            subject='[Web kontakt forma] %s' % cd.get('subject'),
            from_email=settings.NOREPLY_EMAIL,
            to=settings.ADMIN_EMAILS,
            body=cd.get('body'),
            headers={'Reply-To': from_email}
        )
        msg.send()


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        exclude = ['active']
