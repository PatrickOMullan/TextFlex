from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

terms = [

    {
        'term': 'A',
        'title': 'A-Term'
    },
    {
        'term': 'B',
        'title': 'B-Term'
    },
    {
        'term': 'C',
        'title': 'C-Term'
    },
    {
        'term': 'D',
        'title': 'D-Term'
    }
]

def home(request):
    context = {
        'terms': terms,
        'title': 'Select Term'
    }
    return render(request, 'findbooks/select-term.html', context)