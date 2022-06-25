from djchoices import DjangoChoices, ChoiceItem


class SocialType(DjangoChoices):
    twitter = ChoiceItem("twitter")
    google = ChoiceItem("google")
    facebook = ChoiceItem("facebook")

