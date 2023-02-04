from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=False)
    surname = models.CharField(max_length=255, blank=False)


class Food(models.Model):
    name = models.CharField(max_length=255,unique=True,blank=False)
    calories = models.IntegerField(validators=[MinValueValidator(0)])


class Meal(models.Model):

    food = models.ForeignKey("diary.Food", on_delete=models.CASCADE,null=False)
    grams = models.IntegerField(validators=[MinValueValidator(0)])


class Exercise(models.Model):
    name = models.CharField(max_length=255,unique=True,blank=False)
    calories = models.IntegerField(validators=[MinValueValidator(0)])


class Training(models.Model):
    created_at = models.DateTimeField(auto_created=True)
    exercise = models.ForeignKey("diary.Exercise", on_delete=models.CASCADE, null=False)
    reps = models.IntegerField(validators=[MinValueValidator(0)])
    trained_at = models.DateTimeField()


class CompleteTraining(models.Model):
    exercises = models.ManyToManyField("diary.Training")
    total_loss = models.IntegerField(validators=[MinValueValidator(0)])
    total_time = models.IntegerField(validators=[MinValueValidator(0)])
    finished_at = models.DateTimeField()
    executor = models.ForeignKey("diary.Profile", on_delete=models.SET_NULL,null=True)


class CompleteMeal(models.Model):
    meals = models.ManyToManyField("diary.Meal")
    total_gramm = models.IntegerField(validators=[MinValueValidator(0)])
    total_cal = models.IntegerField(validators=[MinValueValidator(0)])
    finished_at = models.DateTimeField()
    consumer = models.ForeignKey("diary.Profile", on_delete=models.SET_NULL,null=True)


class DailyReport(models.Model):
    date = models.DateField()
    activities = models.ManyToManyField("diary.CompleteTraining")
    daily_meals = models.ManyToManyField("diary.CompleteMeal")

