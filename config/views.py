from django.shortcuts import render

def start_page(request):
    return render(request, 'frontend/index.html')
