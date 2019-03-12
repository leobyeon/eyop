from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Code


# Create your views here.
def home(request):
    """ redirects to home page """
    return render(request, 'referral_app/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    if request.method == 'GET':
        form = RegisterForm()
    return render(request, 'referral_app/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'referral_app/profile.html')


class CodesList(ListView):
    model = Code


class CodeCreate(LoginRequiredMixin, CreateView):
    model = Code
    fields = ['code', 'amount', 'UOM', 'criteria']
    success_url = 'codes'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CodeUpdate(LoginRequiredMixin, UpdateView):
    model = Code


class CodeDelete(LoginRequiredMixin, DeleteView):
    model = Code
    success_url = 'codes-list'
