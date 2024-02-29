from django.urls import path
from .views import *
#define here urls 
urlpatterns = [
    path('',view_courses, name='view_courses'),
    path('quiz/<int:cat_id>/',view_quiz),
    path("result/",showPerformance),
    path('addquestion/', add_question, name='add_question'),

]
