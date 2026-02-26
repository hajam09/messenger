from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    user_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.CASCADE)
    last_message = models.DateTimeField(auto_now=True)
    secret = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user_1} and {self.user_2}"

