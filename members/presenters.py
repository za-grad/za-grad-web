from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse


class MemberPresenter(object):

    def __init__(self, model):
        self.model = model

    @property
    def title(self):
        return self.model.name

    @property
    def url(self):
        return self.model.details_url

    @property
    def points(self):
        return self.model.points

    @property
    def __dict__(self):
        return {
            'title': self.title,
            'url': self.url,
            'points': self.points,
        }

    def html(self, template):
        return render_to_string(template, self.__dict__)

    @classmethod
    def qs_to_list(cls, qs, template, offset=0, limit=None):
        qs = qs.select_related('user', 'user__profile', 'district')
        if limit is None:
            limit = settings.IDEA_SMALLBOX_CHUNK_SIZE
        return [cls(el).html(template) for el in qs[offset *
            limit:(offset + 1) * limit]]
