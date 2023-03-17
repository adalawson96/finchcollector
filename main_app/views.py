from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Finch
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

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    #instantiate feedingform to be rendered
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', {
        'finch': finch, 'feeding_form': feeding_form
    })

class FinchCreate(CreateView):
   model = Finch
   fields = '__all__'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['origin', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches'

# POST
def add_feeding(request, finch_id):
    #create a ModelForm instance using the data that was submitted in the form
    form = FeedingForm(request.POST)
    if form.is_valid():
        # we want a model instance but we can't save to the db yet becuase we have not assigned the cat_id FK.
        
