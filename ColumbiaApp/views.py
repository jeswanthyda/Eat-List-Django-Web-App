from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    data = dict()
    import datetime
    data['date'] = datetime.date.today()
    return render(request, "home.html", context=data)

def loggedIn(request):
    data = dict()
    user = request.user
    if user.is_superuser:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            data['message'] = "Successfully processed. Press register again to add another user."
            return render(request,"admin_ops.html", context=data)
        else:
            form = UserCreationForm()
            data['form'] = form
            return render(request,"admin_ops.html",context=data)
    return render(request,"loggedIn.html", context=data)

def register(request):
    #TODO
    pass