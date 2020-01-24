from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from ColumbiaApp.models import Restaurant
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import login as Login
from django.contrib.auth import authenticate

# Create your views here.

def home(request,adminSubmitted=False,adminSubmitData=None):
    data = dict()
    import datetime
    data['date'] = datetime.date.today()
   
    base_template = 'base_nologin.html'

    if request.user.is_authenticated:
        base_template = 'base_login.html'
    
    data['base_template'] = base_template
    user = request.user
    if user.is_superuser:
        if adminSubmitted:
            print(adminSubmitData)
            return render(request,"admin_ops.html", context=adminSubmitData)
        else:
            return render(request,"admin_ops.html")
    return render(request, 'home.html', context=data)

def doLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        Login(request, user)
        return home(request)
    else:
        data = dict()
        data['message'] = "Invalid username of password. Please try again."
        return render(request,'registration/login.html',context=data)

def login(request):
    return render(request,'registration/login.html')

def register(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        return render(request, 'registration/register.html')

def doRegister(request):
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    context = dict()
    try:
        User.objects.get(username=username)
        context['message'] = 'A user with that username already exists. Please try again.'
        return render(request, 'registration/register.html', context)
    except:
        if password1 == password2:
            if User.objects.create_user(username,None, password1).is_active:
                return HttpResponseRedirect(reverse('login'))
            else:
                context['message'] = "User could not be created. Please try again."
                return render(request, 'registration/register.html', context)
        else:
            context['message'] = "Passwords do not match. Please try again."
            return render(request, 'registration/register.html', context)

def doAdminRegister(request):
    username = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    context = dict()
    try:
        User.objects.get(username=username)
        context['message'] = 'A user with that username already exists. Please try again.'
        context['status'] = 'failure'
    except:
        if password1 == password2:
            if User.objects.create_user(username,None, password1).is_active:
                context['message'] = 'User was created successfully.'
                context['status'] = 'success'
            else:
                context['message'] = "User could not be created. Please try again."
                context['status'] = 'failure'
        else:
            context['message'] = "Passwords do not match. Please try again."
            context['status'] = 'failure'
    return home(request, True, context)

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
            new_fav.cuisine = request.GET['cuisine'].capitalize() 
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

def user_profile(request):


    cur_user = request.user
    context = {}
    context['last_name'] = cur_user.last_name
    context['first_name'] = cur_user.first_name
    context['email'] = cur_user.email
    context['display_flag'] = False
    return render(request,'user_profile.html',context)

def user_profile_update(request):
    cur_user = request.user
    cur_user.last_name = request.GET['last_name']
    cur_user.first_name = request.GET['first_name']
    cur_user.email = request.GET['email']
    cur_user.save()
    cur_user = request.user
    context = {}
    context['last_name'] = cur_user.last_name
    context['first_name'] = cur_user.first_name
    context['email'] = cur_user.email
    context['display_flag'] = True
    return render(request, 'user_profile.html', context)