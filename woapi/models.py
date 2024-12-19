from django.db import models

class TransformedCompanyData(models.Model):
    company_name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    open = models.TimeField()
    close = models.TimeField()
    wkday = models.TextField()
    def __str__(self):
        return f"Data Added/Time: {self.id} - {self.timestamp}"