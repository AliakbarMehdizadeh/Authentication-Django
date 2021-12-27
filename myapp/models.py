from django.db import models
from django.conf import settings


# Create your models here.
class UserQuestion(models.Model):
    question = models.CharField(max_length=1000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
