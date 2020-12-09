from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
import threading
from pathlib import Path
from .web_scraper.banner_scrape import run_scrape
from django.contrib.auth.decorators import login_required

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

#THREAD TO GET RESULTS
def scrape_background(year, term, username, password):
    my_file = Path(f'findbooks/web_scraper/json/books_{username}.json')

    if my_file.is_file():
        os.remove(f'findbooks/web_scraper/json/books_{username}.json')

    run_scrape(year, term, username, password)

    return 0


def home(request):
    context = {
        'terms': terms,
        'title': 'Select Term'
    }

    return render(request, 'findbooks/select-term.html', context)

@login_required
def submitA_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }
    
    t1 = threading.Thread(target=scrape_background, args=(2020, "A", username, request.user.profile.Banner_Password,))

    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def submitB_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }

    t1 = threading.Thread(target=scrape_background, args=(2020, "B", username, request.user.profile.Banner_Password,))
    
    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def submitC_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }

    t1 = threading.Thread(target=scrape_background, args=(2021, "C", username, request.user.profile.Banner_Password,))
    
    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def submitD_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }

    t1 = threading.Thread(target=scrape_background, args=(2021, "D", username, request.user.profile.Banner_Password,))
    
    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def submitEI_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }

    t1 = threading.Thread(target=scrape_background, args=(2021, "E1", username, request.user.profile.Banner_Password,))
    
    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def submitEII_Term(request):
    username = request.user.username
    context = {
        'title': 'Loading Results',
        'username': username
    }

    t1 = threading.Thread(target=scrape_background, args=(2021, "E2", username, request.user.profile.Banner_Password,))
    
    t1.start()

    t1.join()

    return redirect(results_page)

@login_required
def results_page(request):
    
    username = request.user.username

    with open(f'findbooks/web_scraper/json/books_{username}.json') as f:
        courses = json.load(f)

        list_to_pass = []

        if len(courses) > 1:
            for course in courses:
                list_to_pass.append(json.dumps(course))
        else:
            list_to_pass = 1

        context = {
            'books': list_to_pass,

            'title': 'Your Books!'
        }

        f.close()

    return render(request, 'findbooks/results-page.html', context)