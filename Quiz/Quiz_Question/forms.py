from django import forms
from .models import QuestionModel

class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ['category', 'question', 'option1', 'option2', 'option3', 'option4', 'time_limit', 'answer']
