from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="term-select"),
    path('results-page/', views.results_page, name='results-page'),
    path('A-Term/', views.submitA_Term, name='A-Term'),
    path('B-Term/', views.submitB_Term, name='B-Term'),
    path('C-Term/', views.submitC_Term, name='C-Term'),
    path('D-Term/', views.submitD_Term, name='D-Term'),
    path('E1-Term/', views.submitEI_Term, name='E1-Term'),
    path('E2-Term/', views.submitEII_Term, name='E2-Term')
]