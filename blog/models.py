from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from idea.models import _generate_upload_path

import re


def blogentry_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname,
        settings.BLOG_ENTRY_IMAGES_ROOT)


def blogauthor_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname,
        settings.BLOG_AUTHOR_IMAGES_ROOT)


class BlogHolder(models.Model):

    class Meta:
        verbose_name = "district"

    district = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, null=True)
    autor_name = models.CharField(max_length=100)
    autor_contact_phone = models.CharField(max_length=255)
    autor_contact_email = models.EmailField()
    autor_image = models.ImageField(upload_to=blogauthor_images_upload_to,
        null=True, blank=True)
    autor_about = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog_entries', args=[self.district.lower()])

    @property
    def autor_image_url(self):
        if self.autor_image and self.autor_image.name:
            return self.autor_image.url
        return ''

    @property
    def last_post(self):
        if not hasattr(self, '_last_post'):
            entries = self.entries.all()
            if len(entries):
                self._last_post = entries[0]
            else:
                self._last_post = None
        return self._last_post

    @property
    def fb_meta(self):
        if self.last_post:
            return self.last_post.fb_meta
        return {}

    def __unicode__(self):
        return self.district

    def save(self, *args, **kwargs):
        self.slug = re.sub('[^\w]+', '-', self.district).lower()
        super(BlogHolder, self).save(*args, **kwargs)


class BlogEntry(models.Model):

    class Meta:
        ordering = ['-date']

    holder = models.ForeignKey(BlogHolder, related_name='entries',
        verbose_name="district")
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to=blogentry_images_upload_to, null=True,
        blank=True)
    date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('blog_entry', args=[self.holder.slug, self.id,
            self.title_slug])

    @property
    def image_url(self):
        if self.image and self.image.name:
            return self.image.url
        return ''

    @property
    def fb_meta(self):
        return {
            'image': self.image_url or self.holder.autor_image_url,
            'title': self.title,
            'content': self.text
        }

    @property
    def share(self):
        return {
            'facebook': 'http://www.facebook.com/share.php?u=http://%s%s' % (
                Site.objects.get_current().domain, self.get_absolute_url()
            ),
            'twitter': 'http://twitter.com/home?status=%s '
            'http://%s%s' % (
                self.title,
                Site.objects.get_current().domain,
                self.get_absolute_url()
            ),
        }

    @property
    def title_slug(self):
        return slugify(self.title)

    def __unicode__(self):
        return self.title


class BlogEntryComment(models.Model):
    class Meta:
        ordering = ['-updated']
    blog_entry = models.ForeignKey(BlogEntry, related_name="comments",
        editable=False)
    author = models.ForeignKey(User, editable=False)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField()
