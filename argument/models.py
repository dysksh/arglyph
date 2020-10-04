from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    advocate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "advocate")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Comment",
        related_name = "author"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    """コメントテーブル"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    