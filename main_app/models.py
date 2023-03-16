from django.db import models
from django.urls import reverse

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

# Create your models here.
class Finch(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    #changing this instance method does not impact the database, therefore no makemigrations is necessaary
    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'finch_id': self.id})
    
class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )

    #create a finch_id fk 
    finch = models.ForeignKey(
        Finch,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
