from django.db import models
from django.utils import timezone


class Task(models.Model):

    title = models.CharField(
        max_length=200,
        verbose_name="Titre",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )

    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date d'échéance",
    )

    due_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure d'échéance",
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Complétée",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )

    def __str__(self):
        return self.title

