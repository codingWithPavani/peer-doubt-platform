from django.db import models

# Create your models here.


# qa/models.py

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    tags = models.CharField(max_length=200)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Answer(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    body = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    votes = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Answer by {self.author.username}"