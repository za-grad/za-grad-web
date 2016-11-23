from django.db import models, transaction
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.validators import MaxLengthValidator

from .signals import idea_approved, idea_disapproved
from .mailer import IdeaMailer

from uuid import uuid4
import os
import re


def _generate_upload_path(instance, fname, root):
    """generate unique path under 'photos' folder"""

    base, ext = os.path.splitext(fname)
    base = uuid4().hex
    dname = os.path.join(root, base[0:2], base[2:4],
        base[4:6])
    fpath = os.path.join(dname, base + ext[:10])
    os.makedirs(os.path.join(settings.MEDIA_ROOT, dname))
    return fpath


def idea_images_upload_to(instance, fname):
    return _generate_upload_path(instance, fname, settings.IDEA_IMAGES_ROOT)


class District(models.Model):

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_choices(cls):
        district_filter_kwargs = {'name': 'CIJELI GRAD'}
        l1 = list(cls.objects.filter(**district_filter_kwargs))
        l2 = list(cls.objects.exclude(**district_filter_kwargs))
        return [(el.id, el.name) for el in l1 + l2]

    def __unicode__(self):
        return self.name


class IdeaCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Idea(models.Model):

    class Meta:
        ordering = ('-vote_diff', '-vote_yes_count')

    user = models.ForeignKey(User, editable=False, related_name='ideas')
    category = models.ForeignKey(IdeaCategory, verbose_name="Kategorija",
        null=True, blank=True)
    district = models.ForeignKey(District, verbose_name="Kvart")
    title = models.CharField(max_length=100, verbose_name="Naslov")
    description = models.TextField(verbose_name="Tekst")
    image = models.ImageField(upload_to=idea_images_upload_to, null=True,
        blank=True, verbose_name="Slika")
    vote_yes_count = models.IntegerField(default=0, editable=False,
        verbose_name="Glasovi ZA")
    vote_no_count = models.IntegerField(default=0, editable=False,
        verbose_name="Glasovi PROTIV")
    vote_diff = models.IntegerField(default=0, editable=False,
        verbose_name="Razlika glasova")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    approved = models.NullBooleanField(verbose_name="Prijedlog odobren?", null=True,
        blank=True, editable=False)

    @property
    def description_html(self):
        return strip_tags(self.description).replace("\n", "<br />")

    def get_absolute_url(self):
        return reverse('idea_details', kwargs={'idea_id': self.id})

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

    def _update_vote_count(self):
        self.vote_yes_count = self.votes.filter(state=True).count()
        self.vote_no_count = self.votes.filter(state=False).count()
        self.vote_diff = self.vote_yes_count - self.vote_no_count
        self.save()

    @transaction.commit_on_success
    def _vote(self, user, state):
        votes = list(self.votes.filter(user=user))
        vote = votes[0] if votes else None
        action = ''
        if vote:
            if vote.state == state:
                vote.delete()
                action = 'delete'
            else:
                vote.state = state
                vote.save()
                action = 'update'
        else:
            vote = self.votes.create(user=user, state=state)
            action = 'create'
        self._update_vote_count()
        self.user.get_profile().recalculate_points()
        user.get_profile().recalculate_points()
        return action

    def vote_yes(self, user):
        return self._vote(user, True)

    def vote_no(self, user):
        return self._vote(user, False)

    def approve(self):
        if self.approved is None:
            self.approved = True
            self.save()
            self.user.get_profile().recalculate_points()
            idea_approved.send(sender=self)

    def disapprove(self, reason):
        if self.approved is None:
            self.approved = False
            self.save()
            idea_disapproved.send(sender=self, reason=reason)

    def __unicode__(self):
        return self.title


class IdeaVote(models.Model):

    class Meta:
        unique_together = ('idea', 'user')

    idea = models.ForeignKey(Idea, related_name='votes')
    user = models.ForeignKey(User, related_name='votes')
    state = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class IdeaCommentManager(models.Manager):
    use_for_related_fields = True

    def valid(self):
        return self.exclude(banned=True)


class IdeaComment(models.Model):

    objects = IdeaCommentManager()

    class Meta:
        ordering = ('-updated',)

    STATE_NEUTRAL = 'neutral'
    STATE_POSITIVE = 'positive'
    STATE_NEGATIVE = 'negative'

    STATES = (
        (STATE_NEUTRAL, 'Neutral comment'),
        (STATE_POSITIVE, 'Positive comment'),
        (STATE_NEGATIVE, 'Negative comment')
    )

    user = models.ForeignKey(User, editable=False, related_name='comments')
    idea = models.ForeignKey(Idea, editable=False, related_name='comments')
    parent_comment = models.ForeignKey('self', editable=False,
        related_name='comments', null=True, blank=True)
    state = models.CharField(max_length=255, choices=STATES,
        default=STATE_NEUTRAL, editable=False)
    comment = models.TextField(validators=[MaxLengthValidator(settings.COMMENT_MAXLENGTH)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    flagged_by = models.ManyToManyField(User, related_name="flagged_comments",
        editable=False)
    banned = models.NullBooleanField(editable=False)

    @property
    def comment_html(self):
        return re.sub('\n\n+', '\n\n', self.comment).replace('\n', '<br>')


@receiver(idea_approved)
def idea_approved_handler(sender, **kwargs):
    IdeaMailer.send_idea_approved_author(sender)


@receiver(idea_disapproved)
def idea_disapproved_handler(sender, reason, **kwargs):
    IdeaMailer.send_idea_disapproved_author(sender, reason)
