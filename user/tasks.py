from django.conf import settings
from celery import shared_task
from celery.utils import log
from user import send_email, email_constant, models

logger = log.get_task_logger(__name__)

@shared_task
def send_auth_email(user_id: int, dynamic_template_data: dict, subject: str, template_id: str):
    try:
        user = models.User.get_user({"id": user_id})
        full_name = f"{user.first_name} {user.last_name}"
        TO_EMAILS = [{"email": user.email, "name": full_name}]
        auth_email = send_email.AuthEmail(settings.EMAIL_FROM, TO_EMAILS, subject)
        auth_email.send_mail(dynamic_template_data=dynamic_template_data, template_id=template_id)
    except Exception as e:
        logger.info(str(e))

