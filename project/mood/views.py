from django.shortcuts import render,redirect
from .models import Mood,Rant
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
import random

# Create your views here.

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render (request,'login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def home(request):
    # mood = Mood.objects.all()
    # total = mood.count()
    # mood_dis = {}
    # for i in mood:
    #     if mood_dis.get(i.rating):
    #         mood_dis[i.rating] += 1
    #     else:
    #         mood_dis[i.rating] = 1
    
    # for i in mood_dis.keys():
    #     mood_dis[i] = round((mood_dis[i]/total)*100,2)

    user = request.user
    try:
        rants = Rant.objects.filter(user = user).order_by('-pk')[:3]
        return render(request, 'home.html',{'rants':rants})
    except Exception:
        return render(request, 'home.html')

def chart(request):
    user = request.user
    avg_data = Mood.objects.filter(user = user).values('created_at').annotate(avg_rating = Avg('rating')).order_by('-created_at')
    labels = []
    values = []
    for en in avg_data:
        rating = en.get('avg_rating')
        round_rating = round(rating)
        rating_dict={1:-2,2:-1,3:1,4:2,5:3}
        values.append(rating_dict.get(round_rating))
        labels.append(rating_dict.get(round_rating))

    data = {
        'labels': labels,
        'data': values,
        'total': sum(values)
    }

    return JsonResponse(data = data)

def rating(request):    
    rating = request.GET.get('rating')
    user = request.user
    mood = Mood(rating=rating,created_at=timezone.now().date(),user=user)
    mood.save()
    
    return JsonResponse({"status":"success"})

def add_rant(request):
    description = request.POST.get('rant')
    user = request.user
    rant = Rant(description=description, created_at=timezone.now().date(), user=user)
    rant.save()

    return redirect('home')

def all_rants(request):
    user = request.user
    rant = Rant.objects.filter(user = user).order_by('-pk')
    return render(request, 'rant.html', {'rants':rant})

def view_rant(request,pk):
    rant = Rant.objects.get(id=pk)
    return render(request, 'view_rant.html', {'rant':rant})

def delete_rant(request,pk):
    rant = Rant.objects.get(id=pk)
    rant.delete()
    return redirect('rants')