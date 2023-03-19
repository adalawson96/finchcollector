from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Finch
from .models import Finch, Toy
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {
        'finches': finches
    })

def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)

def unassoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

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

class FinchCreate(CreateView):
   model = Finch
   fields = ['name', 'origin', 'description', 'age']

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['origin', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

class ToyList(ListView):
    model = Toy
    template_name = 'toys/toy_list.html'

class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/toy_detail.html'

class ToyCreate(CreateView):
    model = Toy
    fields = ('name', 'color')

class ToyUpdate(UpdateView):
    model = Toy
    fields = ('name', 'color')

class ToyDelete(DeleteView):
    model = Toy
    success_url ='/toys'


# POST
def add_feeding(request, finch_id):
    #create a ModelForm instance using the data that was submitted in the form
    form = FeedingForm(request.POST)
    if form.is_valid():
        # we want a model instance but we can't save to the db yet because we have not assigned the cat_id FK.
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id 
        new_feeding.save()
    return redirect('detail', finch_id=finch_id) 

