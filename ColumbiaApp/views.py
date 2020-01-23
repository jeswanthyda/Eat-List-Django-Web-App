from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    data = dict()
    import datetime
    data['date'] = datetime.date.today()
   
    template_name = 'home.html'
    extended_template = 'base_nologin.html'

    if request.user.is_authenticated:
        extended_template = 'base_login.html'
    
    data['extended_template'] = extended_template
    user = request.user
    if user.is_superuser:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            data['message'] = "Successfully processed. Press register again to add another user. "
            return render(request,"admin_ops.html", context=data)
        else:
            form = UserCreationForm()
            data['form'] = form
            return render(request,"admin_ops.html",context=data)
    return render(request, template_name, context=data)

def register(request):
    #TODO
    pass

def restaurant_map(request):
    data = dict()
    return render(request,"restaurant_map.html",context=data)

def fav_list(request):
    #TODO
    # For a given user, get all restaurant entries and send
    # them to fave_list.html
    pass

def add_to_fav(request):
    #TODO
    #Upon adding restaurant from map.
    # Update database here
    pass

def remove_from_fav(request):
    pass