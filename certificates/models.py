from django.db import models
from django.contrib.auth.models import User

class Certificate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    issue_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class CertificateVerification(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE)
    verification_hash = models.CharField(max_length=256)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.certificate.title} - Verified: {self.verified}"
