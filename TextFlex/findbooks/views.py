from django.shortcuts import render
from django.http import HttpResponse
import json
import os
import threading

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
    },
    {
        'term': 'E1',
        'title': 'E1-Term'
    },
    {
        'term': 'E2',
        'title': 'E2-Term'
    }
]

def home(request):
    context = {
        'terms': terms,
        'title': 'Select Term'
    }
    return render(request, 'findbooks/select-term.html', context)

def submitA_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'A'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2020 A {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def submitB_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'B'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2020 B {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def submitC_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'C'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2021 C {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def submitD_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'D'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2021 D {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def submitEI_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'E'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2021 E {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def submitEII_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username,
        'password': 'Oct16ber!!!',
        'term': 'E'
    }

    os.chdir('../web_scraper/')
    
    os.system(f'python banner_scrape.py 2021 E {username} Oct16ber!!!')

    os.chdir('../TextFlex')

    return render(request, 'findbooks/loading-page.html', context)

def results_page(request):
    
    username = request.user.username

    with open(f'../web_scraper/json/books_{username}.json') as f:
        courses = json.load(f)

        print (courses)

        list_to_pass = []

        for course in courses:
            list_to_pass.append(json.dumps(course))

        context = {
            'books': list_to_pass,

            'title': 'Your Books!'
        }

        f.close()

        return render(request, 'findbooks/results-page.html', context)