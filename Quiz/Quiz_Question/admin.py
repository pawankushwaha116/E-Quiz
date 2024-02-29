from django.contrib import admin
from .models import QuestionModel,QuizCategory,Performace
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display=['question','answer']


admin.site.register(QuizCategory)
admin.site.register(QuestionModel)
admin.site.register(Performace)