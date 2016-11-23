# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from .models import Idea, IdeaComment, District, IdeaCategory


class IdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        widgets = {
            # 'category': forms.Select(attrs={
            #     'data-placeholder': 'Odaberi kategoriju'
            # }),
            'district': forms.Select(attrs={
                'data-placeholder': 'Odaberi kvart'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Naslov',
                'class': 'span12'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Opis',
                'rows': 10,
                'class': 'span12'
            }),
            'image': forms.FileInput(attrs={
                'class': 'hide'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = ''
        self.fields['district'].choices = District.get_choices()
        # self.fields['category'].empty_label = ''
        # self.fields['tags'].help_text = ''


class IdeaHoldingJeNasForm(IdeaForm):

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = ''
        self.fields['district'].choices = District.get_choices()[:1]
        self.fields['category'].choices = IdeaCategory.objects.filter(
            name='Holding je naš').values_list('id', 'name')[:1]


class IdeaCommentForm(forms.ModelForm):

    class Meta:
        model = IdeaComment
        widgets = {
            'comment': forms.Textarea(attrs={
                # 'placeholder': 'Tvoj komentar',
                'rows': 2,
                'maxlength': settings.COMMENT_MAXLENGTH,
                'class': 'span12',
                'style': 'width: 100% !important;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(IdeaCommentForm, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.state == IdeaComment.STATE_POSITIVE:
                self.fields['comment'].widget.attrs['placeholder'] = 'Komentiraj zašto si za ovaj prijedlog'
            elif self.instance.state == IdeaComment.STATE_NEGATIVE:
                self.fields['comment'].widget.attrs['placeholder'] = 'Komentiraj zašto si protiv ovog prijedloga'
