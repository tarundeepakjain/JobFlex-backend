from django.db import models

class User(models.Model):
    U_ID = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password_hash = models.TextField()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.uname


class Application(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ]
    id = models.IntegerField(unique=True,default=0)
    APP_ID = models.AutoField(primary_key=True)
    jobrole = models.CharField(max_length=150)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')
    changed_at = models.DateTimeField(auto_now=True)
    link = models.TextField(null=True, blank=True)
    company = models.CharField(max_length=150, null=True, blank=True)
    U_ID = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='U_ID'
    )

    class Meta:
        db_table = 'application'

    def __str__(self):
        return f"{self.jobrole} - {self.company} ({self.status})"


class Email(models.Model):
    email_id = models.AutoField(primary_key=True)
    APP_ID = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        db_column='APP_ID'
    )
    sender = models.CharField(max_length=255, null=True, blank=True)
    emailbody = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    emaildate = models.DateTimeField(auto_now_add=True)
    detected_status = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'email'

    def __str__(self):
        return f"{self.subject} from {self.sender}"


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    U_ID = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='U_ID'
    )
    title = models.CharField(max_length=255)
    blogtext = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title
