from polls.models import Question
from django.http import HttpResponse
from .models import Question

def index(req):
    recent_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in recent_questions])
    return HttpResponse('Recent Questions: '+output)

def detail(req, question_id):
    return HttpResponse('Looking at question: %s' % question_id)