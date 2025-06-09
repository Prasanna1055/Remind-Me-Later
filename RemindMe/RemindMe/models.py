from django.db import models
from django.contrib.auth.models import User

class REMINDME(models.Model):
    srno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    send_via = models.CharField(
        max_length=10,
        choices=[('sms', 'SMS'), ('email', 'Email')],
        default='sms'
    )
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
