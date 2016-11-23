from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

from sorl.thumbnail import get_thumbnail


class PagesSmallBoxPresenter(object):

    def __init__(self, model, item_style='bw'):
        self.model = model
        self.item_style = item_style

    @property
    def title(self):
        return self.model.title

    @property
    def text(self):
        return self.model.content

    @property
    def updated(self):
        return self.model.updated

    @property
    def image(self):
        if self.model.image.name:
            try:
                return get_thumbnail(self.model.image.path, "800x500", crop="center").url
            except:
                return None
        return None

    @property
    def template(self):
        return "pages/news/item.html"

    @property
    def url(self):
        return reverse("page_view", kwargs={'page_name': self.model.page_name})

    @property
    def __dict__(self):
        return {
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'template': self.template,
            'url': self.url,
            'item_style': self.item_style,
            'updated': self.updated,
        }

    @property
    def html(self):
        return render_to_string(self.template, self.__dict__)


class NewsSmallBoxPresenter(PagesSmallBoxPresenter):

    @property
    def url(self):
        return reverse("news_view", kwargs={'news_id': self.model.id})

    @classmethod
    def qs_to_list(cls, qs, offset=0):
        limit = settings.IDEA_SMALLBOX_CHUNK_SIZE
        return [cls(el).html for el in qs[offset * limit:(offset + 1) * limit]]
