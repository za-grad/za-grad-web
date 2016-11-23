from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.template import RequestContext


class IdeaMailer(object):

    @classmethod
    def send_mail_to_user(cls, user, subject, body_html):
        msg = EmailMessage(subject=subject, body=body_html,
            to=[user.get_profile().primary_email])
        msg.content_subtype = "html"
        msg.send()

    @classmethod
    def send_idea_approved_author(cls, idea):
        subject = "Tvoj prijedlog je odobren."
        body_html = render_to_string(
            "mailer/idea/send_idea_approved_author.html",
            RequestContext(HttpRequest(), {'idea': idea})
        )
        cls.send_mail_to_user(idea.user, subject, body_html)

    @classmethod
    def send_idea_disapproved_author(cls, idea, reason):
        subject = "Tvoj prijedlog nije odobren."
        body_html = render_to_string(
            "mailer/idea/send_idea_disapproved_author.html",
            RequestContext(HttpRequest(), {'idea': idea, 'reason': reason})
        )
        cls.send_mail_to_user(idea.user, subject, body_html)
