from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    image = models.ImageField(
        upload_to="materials/course",
        verbose_name="Превью",
        help_text="Загрузите изображение",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание курса", **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    image = models.ImageField(
        upload_to="materials/lesson",
        verbose_name="Превью",
        help_text="Загрузите изображение",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание урока", **NULLABLE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course",
        verbose_name="Курс",
        help_text="Выбирете курс",
    )
    url = models.URLField(
        verbose_name="Ссылка на видео", **NULLABLE
    )

    def __str__(self):
        return f"{self.name}, курс - {self.course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"