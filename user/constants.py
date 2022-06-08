from djchoices import DjangoChoices, ChoiceItem


class RoleType(DjangoChoices):
    admin = ChoiceItem("admin")
    employee = ChoiceItem("employee")
    customer = ChoiceItem("customer")


ACCOUNT_ACTIVATION_EMAIL_SUBJECT = "Active your account!"