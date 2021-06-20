from polls.models import Question
from django.http import Http404
from django.shortcuts import render
from .models import Question

def index(req):
    recent_questions = Question.objects.order_by('-pub_date')[:5]
    data = {
        'recent_questions':recent_questions,
    }
    return render(req, 'polls/index.html', data)

def detail(req, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        data = {
            'question':question,
        }
    except Question.DoesNotExist:
        raise Http404('Question does not exist.')
    return render(req, 'polls/detail.html', data)