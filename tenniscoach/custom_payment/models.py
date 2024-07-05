from django.db import models

# Create your models here.

from payments.models import BasePayment


class Payment(BasePayment):
    pass

    def __str__(self):
        return f"{self.billing_first_name}: Corso {self.description} - {self.total}€"
    
    class Meta:
        verbose_name_plural = "Pagamenti"
        """
        constraints = [
            UniqueConstraint(fields=['billing_first_name', 'description'], name='unique_courseid_username')
        ]
        """