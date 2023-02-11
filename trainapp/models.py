from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.username
    pass


class Food(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    calorie_count = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FoodEntry(models.Model):
    meal_time = models.DateTimeField(default=datetime.now())
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in grams
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def calorie_count(self):
        return round(self.food.calorie_count * (self.weight / 100), 2)

    def __str__(self):
        return f"{self.food.name} ({self.weight}g, {self.calorie_count()} calories)(User:{self.user})"


class Exercise(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    calorie_burn_per_minute = models.PositiveIntegerField()
    calorie_burn_per_rep = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class ExerciseEntry(models.Model):
    date = models.DateField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()  # in minutes
    repeats = models.PositiveIntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def calorie_burn(self):

        return max(round(self.exercise.calorie_burn_per_minute * self.duration, 2),
                   round(self.exercise.calorie_burn_per_minute * self.repeats, 2)
                   )

    def __str__(self):
        return f"{self.exercise.name} ({self.duration} minutes, {self.calorie_burn()} calories)"


class DailyReport(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    workouts = models.ManyToManyField(ExerciseEntry, blank=True)
    food_diary = models.ManyToManyField(FoodEntry, blank=True)

