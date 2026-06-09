from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
