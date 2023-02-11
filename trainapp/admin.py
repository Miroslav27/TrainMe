from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


#class TrainingExerciseInline(admin.TabularInline):
#    model = models.TrainingExercise
#    extra = 1


#class ExerciseAdmin(admin.ModelAdmin):
#    inlines = (TrainingExerciseInline,)


#class TrainingAdmin(admin.ModelAdmin):
#    inlines = (TrainingExerciseInline,)


#class MealContainInline(admin.TabularInline):
 #   model = models.MealContain
 #   extra = 1


#class FoodAdmin(admin.ModelAdmin):
 #   inlines = (MealContainInline,)


#class MealAdmin(admin.ModelAdmin):
#    inlines = (MealContainInline,)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Food)#, FoodAdmin)
#admin.site.register(models.MealContain)
admin.site.register(models.FoodEntry)#, MealAdmin)
admin.site.register(models.Exercise)#, ExerciseAdmin)
#admin.site.register(models.TrainingExercise)
admin.site.register(models.ExerciseEntry)#, TrainingAdmin)