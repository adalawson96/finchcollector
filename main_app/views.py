# import os
# import uuid
# import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy #,Photo
from .forms import FeedingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    # another query
    # finches = request.user.finch_set.all()
    return render(request, 'finches/index.html', {
        'finches': finches
    })

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    #first, create a list of the toy ids that the finch DOes have
    id_list = finch.toys.all().values_list('id')
    #query for the toys that the finch doesn't have by using the exclude() method vs the filter()
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    #instantiate feedingform to be rendered
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch, 
        'feeding_form': feeding_form,  
        'toys': toys_finch_doesnt_have,
    })

class FinchCreate(LoginRequiredMixin, CreateView):
   model = Finch
   fields = ['name', 'origin', 'description', 'age']

    def form_valid(self, form):
        #self.request.user is the logged in user
        form.instance.user = self.request.user
        #let the CreateView's form_valid method do its regular work (saving the object and redirect)
        return super().form_valid(form)   
   
class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['origin', 'description', 'age']

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches'

@login_required
def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

@login_required
def unassoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)


class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ('name', 'color')

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url ='/toys'

# POST
@login_required
def add_feeding(request, finch_id):
    #create a ModelForm instance using the data that was submitted in the form
    form = FeedingForm(request.POST)
    if form.is_valid():
        # we want a model instance but we can't save to the db yet because we have not assigned the cat_id FK.
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id 
        new_feeding.save()
    return redirect('detail', finch_id=finch_id) 

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save the user to the db
            user = form.save()
            # automatically log in the new user
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again!'
    # a bad POST or a GET request so render signup template
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)