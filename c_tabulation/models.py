from django.db import models

# Create your models here.
class CalculatedData(models.Model):
    """ This model is only used for saving search data. Nothing used as of now."""
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    searched_data = models.TextField()