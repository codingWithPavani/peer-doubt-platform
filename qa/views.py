# qa/views.py

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import (
    Question,
    Answer
)

from .forms import (
    QuestionForm,
    AnswerForm
)

from django.contrib.auth.decorators import login_required


def home(request):

    questions = Question.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'qa/home.html',
        {
            'questions': questions
        }
    )


@login_required
def ask_question(request):

    if request.method == 'POST':

        form = QuestionForm(
            request.POST
        )

        if form.is_valid():

            q = form.save(
                commit=False
            )

            q.author = request.user

            q.save()

            return redirect(
                'home'
            )

    else:

        form = QuestionForm()

    return render(
        request,
        'qa/ask_question.html',
        {
            'form': form
        }
    )


@login_required
def question_detail(
        request,
        pk
):

    question = get_object_or_404(
        Question,
        pk=pk
    )

    answers = Answer.objects.filter(
        question=question
    )

    if request.method == 'POST':

        form = AnswerForm(
            request.POST
        )

        if form.is_valid():

            answer = form.save(
                commit=False
            )

            answer.author = request.user

            answer.question = question

            answer.save()

            return redirect(
                'question_detail',
                pk=pk
            )

    else:

        form = AnswerForm()

    return render(
        request,
        'qa/question_detail.html',
        {
            'question': question,
            'answers': answers,
            'form': form
        }
    )


@login_required
def profile(request):

    questions = Question.objects.filter(
        author=request.user
    )

    answers = Answer.objects.filter(
        author=request.user
    )

    return render(
        request,
        'qa/profile.html',
        {
            'questions': questions,
            'answers': answers
        }
    )


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(
        request,
        'qa/register.html'
    )


def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('home')

    return render(
        request,
        'qa/login.html'
    )


def user_logout(request):

    logout(request)

    return redirect('home')