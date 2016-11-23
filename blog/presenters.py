from django.template.loader import render_to_string

from sorl.thumbnail import get_thumbnail


class BlogSidebarPresenter(object):

    def __init__(self, model, item_style='bw'):
        self.model = model
        self.item_style = item_style

    @property
    def title(self):
        return self.model.autor_name

    @property
    def text(self):
        return self.model.autor_about

    @property
    def phone(self):
        return self.model.autor_contact_phone

    @property
    def email(self):
        return self.model.autor_contact_email

    @property
    def image(self):
        if self.model.autor_image.name:
            try:
                return get_thumbnail(self.model.autor_image.path, "800x500",
                    crop="center").url
            except:
                return None
        return None

    @property
    def template(self):
        return "blog/sidebar_item.html"

    @property
    def url(self):
        return None

    @property
    def __dict__(self):
        return {
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'template': self.template,
            'url': self.url,
            'item_style': self.item_style,
            'phone': self.phone,
            'email': self.email,
        }

    @property
    def html(self):
        return render_to_string(self.template, self.__dict__)
