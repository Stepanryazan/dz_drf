from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url and not url.startswith("https://www.youtube.com/"):
            raise ValidationError(
                f"{self.field} должен ссылаться только на видео с сайта youtube.com, "
                f"ссылки на сторонние ресурсы запрещены."
            )