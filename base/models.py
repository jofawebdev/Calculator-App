from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

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
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', help_text="Upload a profile picture (300x300 recommended)")

    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        # Call the original save() method with all parameters.
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
