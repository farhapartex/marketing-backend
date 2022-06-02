from djchoices import DjangoChoices, ChoiceItem


class RoleType(DjangoChoices):
    admin = ChoiceItem("admin")
    employee = ChoiceItem("employee")
    customer = ChoiceItem("customer")

