from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import FoodEntry, ExerciseEntry,Food,Exercise


class FoodEntryForm(forms.ModelForm):
    #calorie_count = forms.IntegerField()

    class Meta:
        model = FoodEntry
        fields = ['meal_time', 'food', 'weight','user']
        widgets = {
            'meal_time': forms.SplitDateTimeWidget,
            'user': forms.HiddenInput,
        }

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)
        print(self.user)

        self.fields['food'].queryset = Food.objects.filter(user=self.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def save(self, commit=True):
        # Get the food name and calorie count from the form data
        food_name = self.cleaned_data['food']
        calorie_count = self.cleaned_data['calorie_count']

        # Try to find an existing Food object with the same name
        try:
            food = Food.objects.get(name=food_name, user=self.user)
        except Food.DoesNotExist:
            # If no matching Food object exists, create a new one
            food = Food.objects.create(name=food_name, calorie_count=calorie_count, user=self.user)

        # Create the DiaryEntry instance with the associated Food object
        entry = super().save(commit=False)
        entry.food = food
        if commit:
            entry.save()
        return entry


class FoodForm(forms.ModelForm):

    class Meta:
        model = Food
        fields = ['name', 'calorie_count', 'user']
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = user