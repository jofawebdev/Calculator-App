from django.db import models
from django.contrib.auth.models import User

class Calculation(models.Model):
    # Operation choices for better readability
    OPERATION_CHOICES = [
        ('add', 'Addition'),
        ('subtract', 'Subtraction'),
        ('multiply', 'Multiplication'),
        ('divide', 'Division'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculations')
    num1 = models.FloatField()
    num2 = models.FloatField()
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at'] # Most recent first
        verbose_name = "Calculation History"
        verbose_name_plural = "Calculation Histories"

    def __str__(self):
        return f"{self.num1} {self.get_operation_symbol()} {self.num2} = {self.result}"
    

    def get_operation_symbol(self):
        """
        Returns mathematical symbol for operation
        """
        symbols = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '÷'
        }
        return symbols.get(self.operation, '')
