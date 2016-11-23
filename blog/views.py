from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .models import BlogHolder, BlogEntry, BlogEntryComment
from .presenters import BlogSidebarPresenter
from .forms import BlogEntryCommentForm

from utils.http import json_response
from utils.views.decorators import require_ajax

import json


def entries(request, slug):
    blog_holder = get_object_or_404(BlogHolder, slug__iexact=slug)
    return render(request, 'blog/base.html', {
        'blog_holder': blog_holder,
        'entries': blog_holder.entries.all(),
        'fb_meta': blog_holder.fb_meta
    })


def entry(request, slug, id, title_slug):
    blog_entry = get_object_or_404(BlogEntry, id=id)
    return render(request, 'blog/base.html', {
        'blog_holder': blog_entry.holder,
        'entries': [blog_entry],
        'fb_meta': blog_entry.fb_meta
    })


def blog_sidebar(request, slug):
    return json_response([BlogSidebarPresenter(el, 'type_two').html
        for el in BlogHolder.objects.filter(slug__iexact=slug)])


def blog_comment_list(request, blog_entry_id):
    blog_entry = get_object_or_404(BlogEntry, id=blog_entry_id)
    html = render_to_string('blog/comments/list.html', RequestContext(
        request, {
            'entry': blog_entry
        }))
    return json_response({
        'html': html
    })


@login_required
@require_ajax
def blog_comment_add(request, blog_entry_id):
    blog_entry = get_object_or_404(BlogEntry, id=blog_entry_id)

    try:
        data = json.loads(request.body)
    except (ValueError, TypeError):
        data = None

    form = BlogEntryCommentForm(data, instance=BlogEntryComment(
        blog_entry=blog_entry, author=request.user))

    if form.is_valid():
        form.save()

    return json_response({})


@login_required
@require_ajax
def blog_comment_delete(request, id):
    blog_entry_comment = get_object_or_404(BlogEntryComment, id=id)
    if request.user == blog_entry_comment.author:
        blog_entry_comment.delete()
    return json_response({})
