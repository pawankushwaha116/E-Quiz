from unicodedata import category
from django.shortcuts import render,redirect
from Quiz_Question.models import QuizCategory,QuestionModel,Performace
from django.http import HttpResponse
from .forms import QuestionForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
# Create your views here.


# Decorator to check if the user is an admin
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponse("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return HttpResponse("Question added successfully!")  # You can redirect to another page if needed
    else:
        form = QuestionForm()
    return render(request, 'add.html', {'form': form})



def true_W(correct_ans, attempt_ans):   #Calculates the number of correct and wrong answers given by the user.
    true = 0
    wrong = 0
    for i in attempt_ans:
        for j in correct_ans:
            if i in correct_ans:
                if attempt_ans[i] == correct_ans[j]:
                    true += 1
    context = {'true': true, "wrong": len(attempt_ans.keys()) - true}
    return context


def findUserAns(requestData): #extract user answers from request data
    qu_id = list(requestData.keys())
    ans_id = list(requestData.values())
    answersheet = dict(zip(qu_id, ans_id))
    if "csrfmiddlewaretoken" in answersheet:
        answersheet.pop("csrfmiddlewaretoken")
    return answersheet


def CorrectAnswer(queryset): #get correct answers from a queryset of questions
    ques = []
    ans = []
    for i in queryset:
        ques.append(str(i.id))
        ans.append(i.answer)
    correct_ans_sheet = dict(zip(ques, ans))
    return correct_ans_sheet


# display quiz categories
def view_courses(request):
    course = QuizCategory.objects.all()
    print(course)
    d1={'course':course}
    resp = render(request,'course.html',context=d1)
    return resp

# filter and display quiz categories based on search query
def view_courses(request):
    query = request.GET.get('q')
    if query:
        course = QuizCategory.objects.filter(title__icontains=query)
    else:
        course = QuizCategory.objects.all()
    
    d1 = {'course': course}
    return render(request, 'course.html', context=d1)

# display quiz questions
def view_quiz(request,cat_id):
    category = QuizCategory.objects.get(id=cat_id)
    question=QuestionModel.objects.filter(category=category)
    d1={'data':question,'category':category}
    correctAns = CorrectAnswer(question)
    if request.method == "POST":
        userAns = findUserAns(request.POST)
        total_ques = len(correctAns.keys())
        total_attempt = len(userAns.keys())

        final = true_W(correctAns, userAns)
    
        point = final["true"] * question[0].category.point
        Performace.objects.create(user=request.user, quize_type=question[0].category,
                                         total_que=total_ques, attempt_que=total_attempt,
                                         points=point, true_que=final["true"],
                                         wrong_que=final["wrong"], result=True)
        return redirect("/Quiz_Question/result")
    return render(request, "quiz.html", {"que_data": question, "quize_category": category})

    return resp

# Displays users performance
def showPerformance(request):
    if request.user.is_authenticated:
        user_performance = Performace.objects.filter(user=request.user).last()
        out_of = user_performance.total_que * user_performance.quize_type.point
        return render(request, "result.html", {"performance": user_performance, "out_of": out_of})
    return HttpResponse(
        "<center><br><br><br><br> User must be Authenticated!!<br>Click here...<a href='/login'>Login</a>")

