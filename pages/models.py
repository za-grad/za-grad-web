# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from idea.models import _generate_upload_path


def page_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname, settings.PAGE_IMAGES_ROOT)


def news_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname, settings.NEWS_IMAGES_ROOT)


class SubDomain(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class PageBaseQuerySet(models.query.QuerySet):

    def subdomain(self, name):
        return self.filter(subdomain__name=name)


class PageBaseManager(models.Manager):

    def subdomain(self, name):
        return self.get_query_set().subdomain(name)

    def get_query_set(self):
        return PageBaseQuerySet(self.model, using=self._db)


class PageBase(models.Model):

    objects = PageBaseManager()

    class Meta:
        ordering = ('-updated',)
        abstract = True

    title = models.CharField(max_length=512)
    content = models.TextField()
    image = models.ImageField(upload_to=page_images_upload_to, null=True,
        blank=True, verbose_name="Slika")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subdomain = models.ForeignKey(SubDomain, null=True, blank=True)

    def __unicode__(self):
        return self.title

    @property
    def share(self):
        return {
            'facebook': 'http://www.facebook.com/share.php?u=http://%s%s' % (
                Site.objects.get_current().domain, self.get_absolute_url()
            ),
            'twitter': 'http://twitter.com/home?status=%s http://%s%s' % (
                self.title,
                Site.objects.get_current().domain,
                self.get_absolute_url()
            ),
        }


class Page(PageBase):

    class Meta:
        unique_together = ['page_name', 'subdomain']

    page_name = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('page_view', kwargs={'page_name': self.page_name})


class News(PageBase):

    def get_absolute_url(self):
        return reverse('news_view', kwargs={'news_id': self.id})


class Membership(models.Model):

    GENDERS = (
        ('musko', 'muško'),
        ('zensko', 'žensko')
    )

    ROLES = (
        ('Volonter', 'Volonter'),
        ('Fundraising', 'Fundraising'),
        ('PR', 'PR'),
        ('Političke komunikacije', 'Političke komunikacije'),
        ('Kreativac', 'Kreativac'),
        ('Pravna pitanja', 'Pravna pitanja'),
        ('Administracija', 'Administracija'),
    )

    active = models.BooleanField(default=False, verbose_name='Aktivan')
    first_name = models.CharField(max_length=50, verbose_name='ime')
    last_name = models.CharField(max_length=50, verbose_name='prezime')
    gender = models.CharField(max_length=10, choices=GENDERS, verbose_name='spol')
    oib = models.CharField(max_length=11, verbose_name='OIB')
    birth_place = models.CharField(max_length=50, verbose_name='mjesto rođenja')
    street = models.CharField(max_length=50, verbose_name='ulica i kućni broj')
    residence = models.CharField(max_length=50, verbose_name='mjesto stanovanja')
    zipcode = models.CharField(max_length=10, verbose_name='poštanski broj')
    district = models.CharField(max_length=50, verbose_name='kvart')
    phone = models.CharField(max_length=20, verbose_name='broj telefona',
        null=True, blank=True, default="")
    mobile = models.CharField(max_length=20, verbose_name='broj mobitela')
    email = models.EmailField(verbose_name='e-mail')
    profession = models.CharField(max_length=50, verbose_name='zanimanje')
    role = models.CharField(max_length=255, null=True, blank=True, choices=ROLES,
        verbose_name='Biste li se aktivirali u radu stranke? Ako da, u kojem dijelu?')
    question_one = models.TextField(null=True, blank=True,
        verbose_name='Kako ste saznali za stranku Za grad?')
    question_two = models.TextField(null=True, blank=True,
        verbose_name='Komentar?')
