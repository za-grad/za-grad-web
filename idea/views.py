# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_GET
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings

from .models import Idea, IdeaComment, District, IdeaCategory
from .forms import IdeaForm, IdeaCommentForm, IdeaHoldingJeNasForm
from .presenters import SmallBoxPresenter

from utils.views.decorators import require_ajax
from utils.http import json_response

import json


def webmaster_tools_html(request):
    return HttpResponse('google-site-verification: google1fc0cb01e90c2212.html')


def test_login(request):
    return json_response({'result': request.user.is_authenticated()})


def homepage(request):
    return redirect('news_list_page')


#########
# IDEAS
#########

@login_required
def create_idea(request):
    if not request.subdomain:
        FormClass = IdeaForm
    elif request.subdomain == 'holdingjenas':
        FormClass = IdeaHoldingJeNasForm
    form = FormClass(request.POST or None, request.FILES or None,
        instance=Idea(user=request.user))
    if form.is_valid():
        form.save()
        messages.info(request, 'Uspješno si predao prijedlog. Nakon što provjerimo da li je prijedlog u skladu s našim statutom poslati ćemo ti odgovor na e-mail.')
        return redirect('idea_list_page')
    return render(request, 'idea/create.html', {
        'form': form,
        'page_name': 'idea_create'
    })


def idea_details(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id, approved=True)
    return render(request, 'idea/details.html', {
        'idea': idea,
    })


@require_GET
def idea_list(request):
    """ returns list of render idea cards """
    # offset
    try:
        offset = int(request.GET.get('offset', 0))
    except ValueError:
        raise Http404

    # initial queryset
    qs = Idea.objects.filter(approved=True)

    if request.subdomain == 'holdingjenas':
        qs = qs.filter(category__name="Holding je naš")

    # filter by user
    filter_user_id = request.GET.get('filter_user_id')
    if filter_user_id:
        qs = qs.filter(user_id=filter_user_id)

    # filter by district
    filter_district_id = request.GET.get('filter_district_id')
    if filter_district_id and filter_district_id != 'all':
        qs = qs.filter(district_id=filter_district_id)

    # filter by category
    filter_category_id = request.GET.get('filter_category_id')
    if filter_category_id and filter_category_id != 'all':
        qs = qs.filter(category_id=filter_category_id)

    # ordering
    order = request.GET.get('order')
    if order == 'latest':
        qs = qs.order_by('-created')
    elif order == 'top':
        qs = qs.order_by('-vote_diff', '-vote_yes_count')

    # render list of idea items (html)
    html_list = SmallBoxPresenter.qs_to_list(qs, request.GET.get(
        'template', 'idea/item.html'), offset)

    # if load_create_link in GET prepend html to html_list
    load_create_link = request.GET.get('load_create_link')
    if load_create_link:
        html_list.insert(0, render_to_string('idea/create_link.html',
            {'STATIC_URL': settings.STATIC_URL}))

    return json_response(html_list)


@require_GET
def advance_idea_list_page(request):
    return render(request, 'idea/advance_list.html', {'page_name': 'idea_list'})


@require_GET
def idea_list_page(request):
    return render(request, 'idea/top_list.html', {'page_name': 'idea_list'})


@require_GET
def district_options(request):
    rendered_options = render_to_string('idea/partials/_district_options.html',
        {'districts': District.get_choices()})
    return json_response({'html': rendered_options})


@require_GET
def category_options(request):
    rendered_options = render_to_string('idea/partials/_category_options.html',
        {'categories': [(el.id, el.name.lower()) for el in IdeaCategory.objects.all()]})
    return json_response({'html': rendered_options})


@require_POST
@require_ajax
@login_required
@user_passes_test(lambda u: u.groups.filter(name='approve_idea').exists())
def approve_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    idea.approve()
    return json_response({})


@require_POST
@require_ajax
@login_required
@user_passes_test(lambda u: u.groups.filter(name='approve_idea').exists())
def disapprove_idea(request, idea_id):
    data = json.loads(request.raw_post_data)
    idea = get_object_or_404(Idea, pk=idea_id)
    idea.disapprove(data['reason'])
    return json_response({})


############
# COMMENTS
############

@login_required
@require_ajax
def create_comment(request, idea_id, state):
    idea = get_object_or_404(Idea, pk=idea_id)
    data = None
    if request.raw_post_data:
        data = json.loads(request.raw_post_data)
    instance = IdeaComment(user=request.user, idea=idea, state=state)
    form = IdeaCommentForm(data, instance=instance)
    form_valid = False
    if form.is_valid():
        form.save()
        form = IdeaCommentForm()
        form_valid = True
    rendered_form = render_to_string(
        'idea/partials/comments/form.html', {'form': form}
    )
    return json_response({'form': rendered_form, 'form_valid': form_valid,
        'state': state})


def comment_list(request, idea_id, state):
    idea = get_object_or_404(Idea, pk=idea_id)
    if request.user.is_authenticated():
        flagged_comments_ids = request.user.get_profile().flagged_comments_ids
    else:
        flagged_comments_ids = []
    comment_list = idea.comments.valid().select_related('user', 'user__profile').filter(state=state)
    rendered_list = render_to_string('idea/partials/comments/list.html', {
        'list': comment_list,
        'flagged_comments_ids': flagged_comments_ids
    })
    return json_response({'list': rendered_list})


def subcomment_list(request, comment_id):
    comment = get_object_or_404(IdeaComment, pk=comment_id)
    rendered_list = render_to_string(
        'idea/partials/comments/subcomment_list.html', {
            'list': comment.comments.all(),
        }
    )
    return json_response({'list': rendered_list})


##########
# VOTING
##########

@login_required
@require_POST
@require_ajax
def vote(request, idea_id, state):
    idea = get_object_or_404(Idea, pk=idea_id)
    if state == 'yes':
        action = idea.vote_yes(request.user)
        if action == 'delete':
            message = 'Obrisan glas ZA prijedlog "%s". ' % idea.title
        else:
            message = 'Dodan glas ZA prijedlog "%s". ' % idea.title
    elif state == 'no':
        action = idea.vote_no(request.user)
        if action == 'delete':
            message = 'Obrisan glas PROTIV prijedloga "%s". ' % idea.title
        else:
            message = 'Dodan glas PROTIV prijedloga "%s". ' % idea.title

    message += "<br>Tvoji bodovi: %d" % request.user.get_profile().points
    return json_response({
        'action': action,
        'yes_count': idea.vote_yes_count,
        'no_count': idea.vote_no_count,
        'message': message
    })


def vote_btns(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    return json_response({
        'yes_btn_html': render_to_string('idea/partials/yes_btn.html', {
            'idea': idea
        }),
        'no_btn_html': render_to_string('idea/partials/no_btn.html', {
            'idea': idea
        }),
    })


############
# FLAGGING
############

@require_POST
@require_ajax
@login_required
def flag_comment(request, comment_id):
    comment = get_object_or_404(IdeaComment, id=comment_id)
    comment.flagged_by.add(request.user)
    return json_response({
        'message': 'Komentar je označen kao spam. Razmotriti ćemo tvoj prijedlog.',
        'html': render_to_string('idea/partials/comments/inner.html',
            {
                'comment': comment,
                'flagged_comments_ids': request.user.get_profile().flagged_comments_ids
            })
    })


@require_POST
@require_ajax
@login_required
def unflag_comment(request, comment_id):
    comment = get_object_or_404(IdeaComment, id=comment_id)
    comment.flagged_by.remove(request.user)
    return json_response({
        'message': 'Komentar nije SPAM.',
        'html': render_to_string('idea/partials/comments/inner.html',
            {
                'comment': comment,
                'flagged_comments_ids': request.user.get_profile().flagged_comments_ids
            })
    })


@require_POST
@require_ajax
@login_required
@user_passes_test(lambda u: u.groups.filter(name='approve_idea').exists())
def ban_comment(request, comment_id):
    comment = get_object_or_404(IdeaComment, id=comment_id)
    comment.banned = True
    comment.save()
    return json_response({})


@require_POST
@require_ajax
@login_required
@user_passes_test(lambda u: u.groups.filter(name='approve_idea').exists())
def unban_comment(request, comment_id):
    comment = get_object_or_404(IdeaComment, id=comment_id)
    comment.banned = False
    comment.save()
    return json_response({})
