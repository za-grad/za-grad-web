# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpRequest

from idea.models import _generate_upload_path
from allauth.account.models import EmailAddress


def idea_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname, settings.MEMBERS_IMAGES_ROOT)


class UserProfileManager(models.Manager):

    @property
    def valid_emailaddresses(self):
        return EmailAddress.objects.select_related('user', 'user__profile')\
            .filter(verified=True, primary=True,
                user__profile__receive_notifications=True)

    @property
    def notification_emails(self):
        for el in self.valid_emailaddresses:
            yield (el.user.profile.name, el.email)

    def send_notification_emails(self, iter_list, subject, html_body,
        include_greeting=False):
        for name, email in iter_list:
            full_html_body = render_to_string(
                'mailer/userprofile/mail_base.html',
                RequestContext(HttpRequest(), {
                    'include_greeting': include_greeting,
                    'html_body': html_body,
                    'name': name
                })
            )
            msg = EmailMessage(subject=subject, body=full_html_body, to=[email])
            msg.content_subtype = "html"
            msg.send()


class UserProfile(models.Model):

    class Meta:
        ordering = ['-points']

    objects = UserProfileManager()

    user = models.OneToOneField(User, related_name="profile", editable=False)
    full_name = models.CharField(max_length=255, blank=True,
        verbose_name="Tvoje Ime:")
    photo = models.ImageField(upload_to=idea_images_upload_to, blank=True,
        null=True)
    approved_ideas_no = models.IntegerField(default=0, editable=False)
    votes_no = models.IntegerField(default=0, editable=False)
    own_ideas_vote_diff = models.IntegerField(default=0, editable=False)
    points = models.FloatField(default=0, null=True, blank=True, editable=False)
    receive_notifications = models.BooleanField(default=True,
        verbose_name="Želim primati obavijesti")

    @property
    def name(self):
        name = ''
        if self.full_name:
            name = self.full_name
        else:
            name = self.user.username
        return name

    @property
    def primary_email(self):
        emails = self.user.emailaddress_set.filter(verified=True, primary=True)
        if emails:
            return emails[0].email
        else:
            return self.user.email

    def recalculate_points(self):
        self.approved_ideas_no, self.votes_no, self.own_ideas_vote_diff = self.game_points
        self.points = self.approved_ideas_no * settings.IDEA_POINT + \
            self.votes_no * settings.VOTE_POINT + \
            self.own_ideas_vote_diff * settings.IDEA_VOTE_DIFF_POINT
        self.save()

    @property
    def game_points(self):
        # affected by:
        # - user's idea is approved
        # - somebody voted for user's idea
        # - user voted
        idea_vote_diff_points = self.approved_ideas.aggregate(
            models.Sum('vote_diff'))['vote_diff__sum']
        if idea_vote_diff_points is None:
            idea_vote_diff_points = 0
        return self.approved_ideas.count(), self.user.votes.count(), idea_vote_diff_points

    @property
    def approved_ideas(self):
        return self.user.ideas.filter(approved=True)

    @property
    def details_url(self):
        return reverse('members_details', kwargs={'id': self.user.id})

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @property
    def flagged_comments_ids(self):
        return list(self.user.flagged_comments.values_list('id', flat=True))


class MobilePhone(models.Model):
    number = models.CharField(max_length=20, unique=True)
