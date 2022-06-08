from django.conf import settings
from user import models, email_constant, tasks, constants


def generate_account_activation_token_send_email( user: models.User):
    # create account activation information
    user_activation_instance = models.UserActivation.create_activation_instance(user)
    # send email to active account
    dynamic_template_data = {
        "name": f"{user.first_name} {user.last_name}",
        "link": f"{settings.FRONTEND_URL}/account-activation?token={user_activation_instance.key}"
    }
    tasks.send_auth_email.delay(user.id, dynamic_template_data, constants.ACCOUNT_ACTIVATION_EMAIL_SUBJECT,
                                email_constant.ACCOUNT_ACTIVATION_TEMPLATE_ID)
