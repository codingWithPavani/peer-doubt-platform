# qa/views.py

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q

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


# def home(request):

#     questions = Question.objects.all().order_by(
#         '-created_at'
#     )

#     return render(
#         request,
#         'qa/home.html',
#         {
#             'questions': questions
#         }
#     )


def home(request):

    query = request.GET.get('q')

    if query:

        # questions = Question.objects.filter(
        #     title__icontains=query
        # ).order_by('-created_at')
        questions = Question.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query) |
        Q(tags__icontains=query)
    ).order_by('-created_at')

    else:

        questions = Question.objects.all().order_by(
            '-created_at'
        )

    return render(
        request,
        'qa/home.html',
        {
            'questions': questions,
            'query': query
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


# @login_required
# def profile(request):

#     questions = Question.objects.filter(
#         author=request.user
#     ).exclude(id__isnull=True)

#     answers = Answer.objects.filter(
#         author=request.user
#     )

#     return render(
#         request,
#         'qa/profile.html',
#         {
#             'questions': questions,
#             'answers': answers
#         }
#     )

from django.contrib.auth.models import User

def profile(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    questions = Question.objects.filter(
        author=user
    )

    answers = Answer.objects.filter(
        author=user
    )

    return render(
        request,
        'qa/profile.html',
        {
            'profile_user': user,
            'questions': questions,
            'answers': answers
        }
    )

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

def register(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # ✅ 2. USER EXISTS CHECK
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'qa/register.html')

        # ✅ 1. PASSWORD CHECK (must STOP execution)
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'qa/register.html')   # 🔥 IMPORTANT

        # ✅ 3. CREATE USER ONLY IF VALID
        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'qa/register.html')


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


def edit_question(request, pk):
    question = Question.objects.get(id=pk)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = QuestionForm(instance=question)

    return render(request, 'qa/edit_question.html', {'form': form})



def delete_question(request, pk):
    question = Question.objects.get(id=pk)

    if request.method == "POST":
        question.delete()
        return redirect('profile')

    return render(request, 'qa/confirm_delete.html', {'question': question})



from django.contrib.auth.models import User

def user_profile(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    questions = Question.objects.filter(author=user)
    answers = Answer.objects.filter(author=user)

    return render(
        request,
        'qa/profile.html',
        {
            'profile_user': user,
            'questions': questions,
            'answers': answers
        }
    )