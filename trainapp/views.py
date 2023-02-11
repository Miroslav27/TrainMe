from django.forms import DateInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FoodEntryForm, FoodForm
from .models import FoodEntry, Food
# FoodInlineFormset
from django import forms

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    fields = ['name', 'calories']
    template_name = 'create_food.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class FoodEntryCreateView(LoginRequiredMixin, CreateView):
    model = FoodEntry
    template_name = "create_meal.html"
    success_url = reverse_lazy("meal_create")
    #fields = "__all__"
    form_class = FoodEntryForm

    def get_form_kwargs(self):
        kwargs = super(FoodEntryCreateView, self).get_form_kwargs()
        kwargs.update({'user':self.request.user})
        return kwargs

    def get_form(self,form_class=None):
        form = super().get_form()
        form.fields["food"].queryset = Food.objects.filter(user=self.request.user)
        form.fields["meal_time"].widget = forms.DateInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_form'] = FoodForm(user=self.request.user)
        return context

    def form_valid(self, form):
        food_id = self.request.POST.get("food")
        if food_id == "0":
            food_name = self.request.POST.get('new_food')
            calorie_count = self.request.POST.get('calorie_count')
            food = Food.objects.create(name=food_name,calorie_count= calorie_count,user=self.request.user)
            form.instance.food = food
        else:
            form.instance.food_id=food_id
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        print(*request)
        return super(FoodEntryCreateView, self).post(request)
"""
class DiaryEntryForm(LoginRequiredMixin, FormView):
    template_name = 'diary/entry_form.html'
    form_class = FoodEntryForm

    def get_initial(self):
        return {'date': self.kwargs['date'],}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['food_form'] = FoodForm(user=self.request.user)
        context['workout_form'] = WorkoutForm(user=self.request.user)
        context['diary_entries'] = DiaryEntry.objects.filter(date=self.kwargs['date'], user=self.request.user)
        return context

    def form_valid(self, form):
        food_form = FoodForm(self.request.user, self.request.POST)
        workout_form = WorkoutForm(self.request.user, self.request.POST)

        if food_form.is_valid():
            food_entry = food_form.save()

            diary_entry = DiaryEntry.objects.create(
                user=self.request.user,
                date=self.kwargs['date'],
                food=food_entry
            )

        if workout_form.is_valid():
            workout_entry = workout_form.save()

            diary_entry = DiaryEntry.objects.create(
                user=self.request.user,
                date=self.kwargs['date'],
                workout=workout_entry
            )

        return super().form_valid(form)

"""


