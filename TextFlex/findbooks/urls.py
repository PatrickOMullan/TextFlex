from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="term-select"),
    path('results-page/', views.results_page, name='results-page'),
    url(r'^submitA-Term', views.submitA_Term),
    url(r'^submitB-Term', views.submitB_Term),
    url(r'^submitC-Term', views.submitC_Term),
    url(r'^submitD-Term', views.submitD_Term),
    url(r'^submitE1-Term', views.submitEI_Term),
    url(r'^submitE2-Term', views.submitEII_Term)
]