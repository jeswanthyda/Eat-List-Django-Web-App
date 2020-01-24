from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from ColumbiaApp.models import Restaurant

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
    if request.user.is_authenticated:
        fav_rest_list = Restaurant.objects.filter(user=request.user)
        data_list = []
        context = {}
        for ele in fav_rest_list:
            temp_dict = {}
            temp_dict['name'] = ele.name
            temp_dict['cuisine'] = ele.cuisine
            temp_dict['url'] = ele.url
            data_list.append(temp_dict)
        context['fav_restaurants'] = data_list
        return render(request,'fav_list.html',context)
    else:
        pass
        #TODO
        #Send to login page

def add_to_fav(request):
    if request.user.is_authenticated:
        cur_user = request.user
        cur_name = request.GET['name']
        try:
            element = Restaurant.objects.get(user=cur_user,name=cur_name)
            context = {'message':'Restaurant already in Favourites!'}
        except:
            new_fav = Restaurant(user=cur_user)
            new_fav.cuisine = request.GET['cuisine']
            new_fav.name = cur_name
            new_fav.save()
            context = {'message':'Successfully Added!'}
        return render(request,'restaurant_map.html',context)
    else:
        #TODO
        #Send to login page
        pass

def remove_from_fav(request):
    if request.user.is_authenticated:
        Restaurant.objects.filter(user=request.user,name=request.GET['res_to_remove']).delete()
        return fav_list(request)
    else:
        pass
        #TODO
        # Send to login page
