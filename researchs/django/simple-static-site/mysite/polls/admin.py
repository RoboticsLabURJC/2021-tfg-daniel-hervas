from polls.models import Question
from django.contrib import admin

from .models import Question

# Register Question object on admin site
admin.site.register(Question)
