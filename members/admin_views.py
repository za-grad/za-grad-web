# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages

from .forms import MassMailForm
from .models import UserProfile


def mass_mail(request):

    if not request.user.is_authenticated():
        return redirect('/admin/')
    if not request.user.groups.filter(name='send_mass_mail').exists():
        raise Http404

    total_recipients = UserProfile.objects.valid_emailaddresses.count()
    form = MassMailForm(request.POST or None)
    if form.is_valid():
        form.send_mails()
        messages.info(request, 'E-mail uspješno poslan.')
        return redirect('members_mass_mail')
    return render(request, 'members/admin/mass_mail.html', {
        'form': form,
        'total_recipients': total_recipients
    })
