from django.shortcuts import render

# Render index.html
def index(request):
    return render(request, 'chat/index.html')
