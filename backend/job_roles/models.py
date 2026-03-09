from django.db import models

class Jobs(models.Model):
    job_id = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=150)
    jobtitle = models.CharField(max_length=150)
    location = models.CharField(max_length=150, null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    postedat = models.DateTimeField(auto_now_add=True)
    link_to_apply = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'jobs'

    def __str__(self):
        return f"{self.jobtitle} at {self.companyname}"