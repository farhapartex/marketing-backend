from djchoices import DjangoChoices, ChoiceItem


class SocialType(DjangoChoices):
    twitter = ChoiceItem("twitter")
    google = ChoiceItem("google")
    facebook = ChoiceItem("facebook")


APP_DICT = {
    "twitter": {
        "title": "Integrate Twitter",
        "description": "Integrate your twitter account by just few clicks. Collect follower information, send promotional messages, observe statistics."
    },
    "telegram": {
        "title": "Integrate Telegram",
        "description": "Integrate your telegram account. Collect user information from groups. Send promotional messages, text. Observe statistics."
    }
}