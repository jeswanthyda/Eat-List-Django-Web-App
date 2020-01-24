from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from ColumbiaApp.models import Restaurant
from django.contrib.auth.models import User
from django.http import JsonResponse


# Create your views here.

def home(request):
    data = dict()
    import datetime
    data['date'] = datetime.date.today()
   
    base_template = 'base_nologin.html'

    if request.user.is_authenticated:
        base_template = 'base_login.html'
    
    data['base_template'] = base_template
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
    return render(request, 'home.html', context=data)

def register(request):
    return render(request, 'registration/register.html')

def doRegister(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        temp_user = form.save()
        User(temp_user)
        return HttpResponseRedirect(reverse('login'))
    else:
        form = UserCreationForm()
        context['form'] = form
        return render(request, 'registration/register.html', context)

def restaurant_map(request):
    data = dict()

    base_template = 'base_nologin.html'

    if request.user.is_authenticated:
        base_template = 'base_login.html'
    
    data['base_template'] = base_template
    return render(request,"restaurant_map.html",context=data)

def fav_list(request):
    context=dict()
    if request.user.is_authenticated:
        fav_rest_list = Restaurant.objects.filter(user=request.user)
        data_list = []
        for ele in fav_rest_list:
            temp_dict = {}
            temp_dict['name'] = ele.name
            temp_dict['cuisine'] = ele.cuisine
            temp_dict['url'] = ele.url
            data_list.append(temp_dict)
        context['fav_restaurants'] = data_list
        return render(request,'fav_list.html',context)
    else:
        return HttpResponseRedirect(reverse('login'))

def add_to_fav(request):
    if request.user.is_authenticated:
        cur_user = request.user
        cur_name = request.GET['name']
        try:
            element = Restaurant.objects.get(user=cur_user,name=cur_name)
            context = {'message': 'The restaurant is already in your favorites!'}
            context['m_type'] = "info"
            return JsonResponse(context)
        except:
            new_fav = Restaurant(user=cur_user)
            new_fav.cuisine = request.GET['cuisine']
            new_fav.name = cur_name
            new_fav.save()
            context = {'message':'The restaurant is added to your favorites!'}
            context['m_type'] = "success"
            return JsonResponse(context)
    else:
        context = {'message':'Unfortunately, you are not logged in. Click \
        <a href=\'/login\'>here</a> to login'}
        context['m_type'] = "failure"
        return JsonResponse(context)


def remove_from_fav(request):
    if request.user.is_authenticated:
        Restaurant.objects.filter(user=request.user,name=request.GET['res_to_remove']).delete()
        return fav_list(request)
    else:
        return HttpResponseRedirect(reverse('login'))

