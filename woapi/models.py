from django.db import models


class TransformedCompanyData(models.Model):
    company_name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    open = models.TimeField()
    close = models.TimeField()
    day = models.TextField()

    def __str__(self):
        return f"ParsedData: {self.id} - {self.timestamp}"