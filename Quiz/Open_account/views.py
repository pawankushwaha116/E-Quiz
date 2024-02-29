from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method=="GET":
        resp = render(request,'signup.html')
        return resp
    
    elif request.method=="POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        myuser = User.objects.create_user(username=username, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.email=email
        myuser.pass2=pass2
        myuser.save()
        messages.success(request, "Your Account Created Successfully...")
    resp = render(request,'signup.html')
    return resp

def loginUser(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            pass1 = request.POST['pass1']

            user = authenticate(username=username, password=pass1)
            print(user, "<----user")
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return redirect("/Quiz_Question")
            else:
                messages.error(request, "Invalid credentials! Please try again")
        return render(request, 'login.html')
    else:
        return redirect("/Quiz_Question")


def signout(request):
    logout(request)
    messages.success(request, 'You are successfully logout')
    return redirect('/')