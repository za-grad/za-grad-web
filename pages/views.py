# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .presenters import PagesSmallBoxPresenter, NewsSmallBoxPresenter
from .models import Page, News
from .forms import ContactForm, MembershipForm

from utils.http import json_response


# @require_GET
# def pages_list(request):
#     pages = []
#     try:
#         news = News.objects.latest('updated')
#         pages.append(NewsSmallBoxPresenter(news).html)
#     except News.DoesNotExist:
#         pass
#     pages.extend([PagesSmallBoxPresenter(el).html for el in Page.objects.all()])
#     return json_response(pages)


def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


def sidebar_pages_list(request):
    return json_response([PagesSmallBoxPresenter(el, 'type_two').html
        for el in Page.objects.filter(
            Q(page_name='uclani-se') | Q(page_name='program'))])


def page_view(request, page_name):
    try:
        page = Page.objects.get(page_name=page_name, subdomain__name=request.subdomain)
    except Page.DoesNotExist:
        page = get_object_or_404(Page, page_name=page_name)
    return render(request, 'pages/specific/%s.html' % page_name, {'page': page,
        'page_name': page_name})


def page_view_as_partial(request, page_name):
    try:
        page = Page.objects.get(page_name=page_name, subdomain__name=request.subdomain)
    except Page.DoesNotExist:
        page = get_object_or_404(Page, page_name=page_name)
    html = render_to_string('pages/partials/details.html',
        RequestContext(HttpRequest(), {'page': page, 'page_name': page_name}))
    return HttpResponse(html)


def news_view(request, news_id):
    news = get_object_or_404(News, pk=news_id)
    return render(request, 'pages/news/base.html', {'page': news})


def contact_page(request):
    form = ContactForm(request.POST or None)
    try:
        text = Page.objects.get(page_name='kontakt').content
    except Page.DoesNotExist:
        text = ''
    if form.is_valid():
        form.send()
        messages.info(request, 'Tvoja poruka je uspješno zaprimljena. Odgovorit ćemo ti u najkraćem mogućem roku.')
        return redirect('contact_page')
    return render(request, 'pages/specific/contact.html', {
        'form': form,
        'page_name': 'contact',
        'text': text
    })


@login_required
def membership_form_page(request):
    form = MembershipForm(request.POST or None)
    try:
        text = Page.objects.get(page_name='uclani-se').content
    except Page.DoesNotExist:
        text = ''
    if form.is_valid():
        model = form.save()

        # send mail
        subject = "Tvoja pristupnica za članstvo je zaprimljena."
        body_html = render_to_string("mailer/membership/after_form_submit.html")
        msg = EmailMessage(subject=subject, body=body_html, to=[model.email])
        msg.content_subtype = "html"
        msg.send()

        if settings.MEMBERSHIP_ADMIN_EMAILS:
            admin_body_html = render_to_string("mailer/membership/after_form_submit_admin.html",
                RequestContext(HttpRequest(), {}))
            admin_msg = EmailMessage(subject='Novi korisnik ispunio je pristupnicu',
                body=admin_body_html, to=settings.MEMBERSHIP_ADMIN_EMAILS)
            admin_msg.content_subtype = "html"
            admin_msg.send()

        messages.info(request, 'Tvoja pristupnica za članstvo je zaprimljena. Kontaktirati ćemo te uskoro.')
        return redirect('membership_form_page')
    return render(request, 'pages/specific/uclani-se.html', {
        'form': form,
        'page_name': 'uclani-se',
        'text': text
    })


@require_GET
def news_list(request):
    try:
        offset = int(request.GET.get('offset', 0))
    except ValueError:
        raise Http404
    return json_response(NewsSmallBoxPresenter.qs_to_list(
        News.objects.filter(subdomain__name=request.subdomain), offset))


@require_GET
def news_list_page(request):
    return render(request, 'pages/news/list.html', {'page_name': 'news_list'})
