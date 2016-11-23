from django.conf import settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpRequest

from sorl.thumbnail import get_thumbnail


class SmallBoxPresenter(object):

    def __init__(self, model):
        self.model = model

    @property
    def title(self):
        return self.model.title

    @property
    def text(self):
        return self.model.description_html

    @property
    def image(self):
        if self.model.image.name:
            try:
                return get_thumbnail(self.model.image.path, "800x500", crop="center").url
            except:
                return None
        return None

    @property
    def url(self):
        return reverse("idea_details", kwargs={'idea_id': self.model.id})

    @property
    def when(self):
        return self.model.created.date()

    @property
    def who(self):
        return self.model.user.get_profile().name

    @property
    def points(self):
        return self.model.vote_diff

    @property
    def district(self):
        return self.model.district.name.lower()

    @property
    def category(self):
        if self.model.category:
            return self.model.category.name.lower()

    @property
    def __dict__(self):
        return {
            'title': self.title,
            'text': self.text,
            'image': self.image,
            # 'template': self.template,
            'url': self.url,
            'who': self.who,
            'when': self.when,
            'yes_count': self.model.vote_yes_count,
            'no_count': self.model.vote_no_count,
            'points': self.points,
            'district': self.district,
            'category': self.category,
            'item_style': 'bw',
        }

    def html(self, template):
        context = RequestContext(HttpRequest(), self.__dict__)
        return render_to_string(template, context)

    @classmethod
    def qs_to_list(cls, qs, template, offset=0):
        qs = qs.select_related('user', 'user__profile', 'district')
        limit = settings.IDEA_SMALLBOX_CHUNK_SIZE
        return [cls(el).html(template) for el in qs[offset * limit:(offset + 1) * limit]]
