from django.shortcuts import render

# Create your views here.

def home(request):
    data = dict()
    import datetime
    data['date'] = datetime.date.today()
    return render(request, "home.html", context=data)