from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(
        verbose_name="Email", unique=True, help_text="Укажите почту"
    )
    phone = models.CharField(
        verbose_name="Телефон", max_length=35, help_text="Укажите телефон", **NULLABLE
    )
    city = models.CharField(
        verbose_name="Город", max_length=35, help_text="Укажите город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите фото профиля",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежей"""

    METHOD_CHOICES = [
        ("Cash", "Оплата наличными"),
        ("Non-cash", "Безналичный расчет"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_payment",
        verbose_name="Пользователь",
        **NULLABLE,
    )
    date_of_payment = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="Сумма платежа", help_text="Введите сумму платежа"
    )
    payment_method = models.CharField(
        verbose_name="Способ оплаты",
        max_length=100,
        help_text="Выберите способ оплаты",
        choices=METHOD_CHOICES,
    )
    session_id = models.CharField(max_length=255, verbose_name="ID сессии", **NULLABLE)
    payment_link = models.URLField(
        max_length=400, verbose_name="Ссылка на оплату", **NULLABLE
    )

    def __str__(self):
        return (
            f"{self.user}: {self.date_of_payment}, {self.payment_amount}, {self.payment_method}, "
            f"за {self.paid_course if self.paid_course else self.paid_lesson}"
        )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"