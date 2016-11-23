from django import forms
from .models import BlogEntryComment


class BlogEntryCommentForm(forms.ModelForm):
    class Meta:
        model = BlogEntryComment
