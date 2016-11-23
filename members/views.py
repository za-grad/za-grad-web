# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.http import require_POST

from .forms import UserProfileForm
from .models import UserProfile, MobilePhone
from .presenters import MemberPresenter

from utils.http import json_response
from utils.views.decorators import require_ajax

import json
import re


@login_required
def profile_edit(request):
    form = UserProfileForm(request.POST or None, request.FILES or None,
        instance=request.user.get_profile())
    if form.is_valid():
        form.save()
        return redirect('members_edit_profile')
    return render(request, 'members/edit_profile.html', {
        'form': form
    })


def details(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, 'members/details.html', {
        'profile': user.get_profile()
    })


def member_list_ajax(request):
    try:
        offset = int(request.GET.get('offset', 0))
    except ValueError:
        raise Http404

    qs = UserProfile.objects.exclude(user__emailaddress__verified=False)\
        .filter(points__gt=0).distinct()

    html_list = MemberPresenter.qs_to_list(qs, request.GET.get(
        'template', 'partials/small_item.html'), offset)

    return json_response(html_list)


def member_list(request):
    return render(request, 'members/list.html', {'page_name': 'member_list'})


@require_ajax
@require_POST
def mobile_form_handler(request):
    success_response = {'success': True, 'msg': 'Uspješno ste predali broj mobitela. Hvala!'}
    fail_response = {'success': False, 'msg': 'Neispravan broj.'}

    try:
        data = json.loads(request.body)
    except:
        return json_response(fail_response)

    mobile = re.sub('[^0-9]', '', data['mobile'])
    if len(mobile) not in [9, 10]:
        return json_response(fail_response)

    MobilePhone.objects.get_or_create(number=mobile)

    return json_response(success_response)


def give_mobile_page(request):
    return render(request, 'members/give_mobile.html', {})
