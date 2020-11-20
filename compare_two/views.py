from django.shortcuts import render

# Create your views here.

def search_by_isbn(request):
    return render(request, 'comparation.html')