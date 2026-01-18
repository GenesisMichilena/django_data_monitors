from django.db import models

class DashboardModel(models.Model):
    name = models.CharField(max_length=100, default="Dashboard")
    
    class Meta:
        permissions = [
            ("index_viewer", "Can show to index view (function-based)"),
        ]
    
    def __str__(self):
        return self.name
