from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.http import HttpResponse


# Create your views here.
def home(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        print(category_id)
        return redirect('question', category_id=category_id)
    else:
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, "home.html", context)


def question(request, category_id):
    questions = QuestionModel.objects.filter(category_id=category_id)
    total_questions = len(questions)
    # Get the current question index from the session data
    question_index = request.session.get('question_index', 0)

    if question_index >= total_questions:
        # All questions have been answered, redirect to result page
        return redirect('result')

    current_question = questions[question_index]
    if request.method == 'POST':
        selected_answer = request.POST.get(f"question-{current_question.pk}")
        if selected_answer == current_question.answer:
            # Increase the score if the answer is correct
            request.session['score'] = request.session.get('score', 0) + 1
            request.session['correct'] = request.session.get('correct', 0) + 1
            request.session['total'] = request.session.get('total', 0) + 1
        else:
            request.session['wrong'] = request.session.get('wrong', 0) + 1
            request.session['total'] = request.session.get('total', 0) + 1

        # Increase the question index
        request.session['question_index'] = question_index + 1

    # Check if the user was redirected from the timer
    next_question = request.GET.get('next_question')
    if next_question:
        if question_index >= total_questions-1:
        # All questions have been answered, redirect to result page
            return redirect('result')
        else:
            # Increment the question index
            request.session['question_index'] = question_index + 1
            current_question = questions[question_index + 1]
            return redirect('question', category_id=category_id)

    context = {
        'question': current_question,
        'question_index': question_index,
        'total_questions': total_questions,
    }
    return render(request, 'questions.html', context)




def result(request):
    question_index = request.session.get('question_index')
    total_questions = len(QuestionModel.objects.all())

    if question_index != total_questions:
        # Redirect the user back to the home page if they haven't answered all questions yet
        return redirect('home')

    score = request.session.get('score', 0)
    correct = request.session.get('correct', 0)
    wrong = request.session.get('wrong', 0)
    total = request.session.get('total', 0)
    context = {
        'score': score,
        'correct': correct,
        'wrong': wrong,
        'total': total
    }

    # Reset session data
    request.session['score'] = 0
    request.session['correct'] = 0
    request.session['wrong'] = 0
    request.session['total'] = 0
    request.session['question_index'] = 0

    return render(request, "result.html", context)


def play_again(request):
    return redirect('home')
