from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseServerError, HttpResponseNotFound

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return render(request, 'home.html')

@login_required
def index(request):
    context = {
        'segment': 'dashboard',
        'page_title': 'Dashboard',
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def profile(request):
    context = {
        'segment': 'profile',
        'page_title': 'User Profile',
    }
    return render(request, 'dashboard/profile.html', context)

@login_required
def tables(request):
    context = {
        'segment': 'tables',
        'page_title': 'Tables',
    }
    return render(request, 'dashboard/tables.html', context)

# Context processor
def site_settings(request):
    return {
        'site_name': 'Soft UI Dashboard',
        'site_url': 'https://django-soft-ui-free.appseed-srv1.com/',
    }

# Error Handlers
def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

class Error404View(TemplateView):
    template_name = 'errors/404.html'

class Error500View(TemplateView):
    template_name = 'errors/500.html'
