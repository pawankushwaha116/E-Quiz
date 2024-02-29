from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class QuizCategory(models.Model):
    title = models.CharField(max_length=200, null=True,unique=True)
    details = models.TextField(max_length=200,null=True,blank=True)
    point=models.PositiveIntegerField()

    class Meta:
        verbose_name_plural ='Categories'

    def __str__(self):
        return self.title
        
class QuestionModel(models.Model):
    category = models.ForeignKey(QuizCategory,on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    option1 = models.CharField(max_length=200,null=True,blank=True)
    option2 = models.CharField(max_length=200,null=True,blank=True)
    option3 = models.CharField(max_length=200,null=True,blank=True)
    option4 = models.CharField(max_length=200,null=True,blank=True)
    time_limit = models.IntegerField()
    answer = models.CharField(max_length=200,null=True, blank=True)

    class Meta:
        verbose_name_plural ='QuestionModel'

    def __str__(self):
        return self.question

class Performace(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quize_type=models.ForeignKey(QuizCategory,to_field="title",on_delete=models.CASCADE)
    total_que=models.PositiveIntegerField()
    attempt_que=models.PositiveIntegerField()
    points=models.PositiveBigIntegerField()
    true_que=models.PositiveIntegerField()
    wrong_que=models.PositiveIntegerField()
    result=models.BooleanField(blank=True,null=True)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)+"  "+str(self.quize_type)
