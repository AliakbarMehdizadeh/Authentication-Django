from django.shortcuts import render, redirect
from .forms import NewUserForm
from .forms import NewQuestion
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import UserQuestion


# Create your views here.
def homepage(request):
    return render(request=request, template_name='myapp/home.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("myapp:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="myapp/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("myapp:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="myapp/login.html", context={"login_form": form})


def get_question(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewQuestion(request.POST)
        # check whether it's valid:
        if form.is_valid():
            obj = form.save(commit=False)  # Return an object without saving to the DB
            obj.author = User.objects.get(pk=request.user.id)  # Add an author field
            obj.save()
            return redirect("myapp:answer")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewQuestion()
    return render(request=request, template_name='myapp/question.html', context={'form': form})


def post_answer(request):
    questions = UserQuestion.objects.all()
    return render(request=request, template_name="myapp/answer.html", context={'questions': questions})
