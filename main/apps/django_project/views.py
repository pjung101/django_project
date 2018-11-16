from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from .models import User, Wish, Like
import bcrypt

# Create your views here.
def index(request):
    if 'id' in request.session.keys():
        request.session.clear()
    if 'first_name' not in request.session.keys():
        request.session['first_name'] = ''
        request.session['last_name'] = ''
        request.session['email'] = ''
        request.session['lemail'] = ''
    return render(request,"django_project/index.html")
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/')
        else:
            User.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            request.session['id'] = User.objects.last().id
            request.session['first_name'] = User.objects.last().first_name
            return redirect('/wishes')
    return redirect('/')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/')
        request.session['id'] = User.objects.get(email=request.POST['lemail']).id
        request.session['first_name'] = User.objects.get(email=request.POST['lemail']).first_name
        return redirect('/wishes')
def wishes(request):
    if 'id' not in request.session.keys():
        return redirect('/')
    selected_w = Wish.objects.all()
    selected_l = Like.objects.all()
    selected_u = User.objects.get(id = request.session['id']).likes.all().values()
    arr = []
    for i in selected_u:
        arr.append(i['wish_id'])
    print(arr)

    context = {
            'selected_w':selected_w,
            'selected_l':selected_l,
            'selected_u':arr
            }
    return render(request,"django_project/wishes.html", context)
def new(request):
    if 'id' not in request.session.keys():
        return redirect('/')
    return render(request,"django_project/new.html")
def create(request):
    if 'id' not in request.session.keys():
        return redirect('/')
    errors = Wish.objects.wish_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/wishes/new')
        Wish.objects.create(item = request.POST['item'],desc = request.POST['desc'], user = User.objects.get(id=request.session['id']), granted = 0)
        return redirect('/wishes')
    return redirect('/wishes')
def like(request,id):
    if 'id' not in request.session.keys():
        return redirect('/')
    Like.objects.create(wish = Wish.objects.get(id=id), user = User.objects.get(id=request.session['id']))
    return redirect('/wishes')
def delete(request,id):
    if 'id' not in request.session.keys():
        return redirect('/')
    Wish.objects.get(id = id).delete()
    return redirect('/wishes')
def stats(request):
    if 'id' not in request.session.keys():
        return redirect('/')
    selected_l = Like.objects.all()
    a = len(selected_l)
    print(a)
    b = len(Wish.objects.filter(user = User.objects.get(id = request.session['id']), granted = 0))
    c = len(Wish.objects.filter(user = User.objects.get(id = request.session['id']), granted = 1))
    context = {
            'a':a,
            'b':b,
            'c':c
            }
    return render(request, "django_project/stats.html", context)
def edit(request,id):
    if 'id' not in request.session.keys():
        return redirect('/')
    p = Wish.objects.get(id = id)
    request.session['item'] = p.item
    request.session['desc'] = p.desc
    context = {
            'p':p
            }
    return render(request,"django_project/edit.html", context)
def update(request,id):
    if 'id' not in request.session.keys():
        return redirect('/')
    errors = Wish.objects.wish_validator(request.POST)
    if request.method == 'POST':
        if len(errors):
            for key, value in errors.items():
                messages.error(request,value, extra_tags = key)
            return redirect('/wishes/edit/'+ str(id))
        p = Wish.objects.get(id = id)
        p.item = request.POST['item']
        p.desc = request.POST['desc']
        p.save()
        request.session['item'] = ''
        request.session['desc'] = ''
        return redirect('/wishes')
    return redirect('/wishes')

def logout(request):
    request.session.clear()
    return redirect('/')
def granted(request, id):
    if 'id' not in request.session.keys():
        return redirect('/')
    a = Wish.objects.get(id = id)
    a.granted = 1
    a.save()
    return redirect('/wishes')
