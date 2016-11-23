from django.conf.urls.defaults import patterns, url
from .views import *
from .models import IdeaComment


urlpatterns = patterns('',

    # voting
    url(r'^(?P<idea_id>\d+)/vote/(?P<state>(yes|no))/$', vote,
        name='idea_vote'),
    url(r'^(?P<idea_id>\d+)/vote_btns/$', vote_btns,
        name='idea_vote_btns'),

    # comments
    url(r'^(?P<idea_id>\d+)/comment/(?P<state>%s)/create/$' %
        ('|'.join(dict(IdeaComment.STATES).keys())), create_comment,
        name='idea_create_comment'),
    url(r'^(?P<idea_id>\d+)/comment/(?P<state>%s)/list/$' %
        ('|'.join(dict(IdeaComment.STATES).keys())), comment_list,
        name='idea_comment_list'),
    url(r'^comment/(?P<comment_id>\d+)/subcomment/list/$', subcomment_list,
        name='idea_subcomment_list'),
    url(r'^comment/(?P<comment_id>\d+)/flag/$', flag_comment,
        name='idea_comment_flag'),
    url(r'^comment/(?P<comment_id>\d+)/unflag/$', unflag_comment,
        name='idea_comment_unflag'),
    url(r'^comment/(?P<comment_id>\d+)/ban/$', ban_comment,
        name='idea_comment_ban'),
    url(r'^comment/(?P<comment_id>\d+)/unban/$', unban_comment,
        name='idea_comment_unban'),

    # idea
    url(r'^detaljno/$', advance_idea_list_page, name='advance_idea_list_page'),
    url(r'^$', idea_list_page, name='idea_list_page'),

    url(r'^list/$', idea_list, name='idea_list'),
    url(r'^(?P<idea_id>\d+)/$', idea_details, name='idea_details'),
    url(r'^daj/$', create_idea, name='idea_create'),

    url(r'^(?P<idea_id>\d+)/approve/', approve_idea, name='idea_approve'),
    url(r'^(?P<idea_id>\d+)/disapprove/', disapprove_idea, name='idea_disapprove'),

    url(r'^district_options/', district_options, name='idea_district_options'),
    url(r'^category_options/', category_options, name='idea_category_options')

)
