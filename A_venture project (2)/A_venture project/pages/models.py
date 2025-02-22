from django.db import models
from auditlog.registry import auditlog
#done
class User(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]

    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Record(models.Model):

    label_choices = [
        ('accepting', 'accepting'),
        ('rejecting', 'rejecting'),
    ]
    record_id = models.AutoField(primary_key=True)
    code = models.TextField()
    wilaya = models.TextField()
    field = models.TextField()
    activity = models.TextField()
    description = models.TextField()
    label = models.CharField(max_length=12, choices=label_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


auditlog.register(Record)
auditlog.register(User)