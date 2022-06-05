import os
import typing
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from user import email_constant

"""
Documentation: https://docs.sendgrid.com/api-reference/mail-send/mail-send#handlebars
"""

class BaseAbstractEmail:
    def __init__(self, from_email: str, to_emails: typing.List[typing.Dict], subject: str):
        self.sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.to_emails = to_emails
        self.subject = subject
        self.from_email = from_email
        self.mail = None
        self.__initialize_mail()

    def __initialize_mail(self):
        self.mail = Mail()
        self.mail.to = [
            To(
                email=to_email["email"],
                name=to_email["name"]
            ) for to_email in self.to_emails
        ]
        self.mail.from_email = From(
            email=self.from_email,
            name="Team Insight"
        )
        self.mail.reply_to = ReplyTo(
            email=self.from_email,
            name="Team Insight"
        )
        self.mail.subject = Subject(self.subject)
        self.mail.content = [
            Content(
                mime_type="text/html",
                content="<p></p>"
            )
        ]
        self.mail.mail_settings = MailSettings(
            bypass_list_management=BypassListManagement(False),
            footer_settings=FooterSettings(False),
            sandbox_mode=SandBoxMode(False)
        )

        self.mail.tracking_settings = TrackingSettings(
            click_tracking=ClickTracking(
                enable=True,
                enable_text=False
            ),
            open_tracking=OpenTracking(
                enable=True,
                substitution_tag=OpenTrackingSubstitutionTag("%open-track%")
            ),
            subscription_tracking=SubscriptionTracking(False)
        )

    def send_mail(self):
        raise NotImplementedError("Must implement api call function")


class AuthEmail(BaseAbstractEmail):
    # This class is responsible to send email for registration confirm, account activation confirm
    def __init__(self, from_email, to_emails, subject):
        super(AuthEmail, self).__init__(
            from_email=from_email, to_emails=to_emails, subject=subject
        )

    def send_mail(self, dynamic_template_data=None, template_id=None, html_content=None):
        if dynamic_template_data and template_id:
            self.mail.template_id = template_id
            self.mail.dynamic_template_data = dynamic_template_data
        else:
            self.mail.content = [
                Content(
                    mime_type="text/html",
                    content=html_content
                )
            ]

        self.sendgrid_client.send(self.mail)


