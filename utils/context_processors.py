from django.contrib.sites.models import Site
from django.conf import settings

from blog.models import BlogHolder


def site_processor(request):
    current_domain = Site.objects.get_current().domain
    return {
        'BANNER_URL': '/',  # "http://holdingjenas.%s" % current_domain,
        'SITE_URL': "http://%s" % current_domain,
        'TWITTER_PAGE': settings.TWITTER_PAGE,
        'FACEBOOK_PAGE': settings.FACEBOOK_PAGE,
        'IDEA_POINT': settings.IDEA_POINT,
        'VOTE_POINT': settings.VOTE_POINT,
        'IDEA_VOTE_DIFF_POINT': settings.IDEA_VOTE_DIFF_POINT,
        'BLOGS': [(el.slug, el.district) for el in
            BlogHolder.objects.exclude(entries=None)]
    }
