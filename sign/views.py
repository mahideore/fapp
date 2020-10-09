from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from sign.models import Services,servicecreate,contact
from django.middleware import csrf


# Create your views here.
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == "POST":
        # CHECK IF A USER EXITS OR NOT
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        if user is not None:
            auth.login(request, user)
            token = request.META.get('CSRF_COOKIE', None)
            if token is None:
                token = csrf.get_token(request)
                print("e", token)
                request.META['CSRF_COOKIE'] = token
            print("tokennnnn",token)
            request.META['CSRF_COOKIE_USED'] = True
            print(user.__dict__)
            if user.is_superuser:
                return render(request, 'admin_home.html')
            # todo : check for service provider and clint
            return render(request, 'show.html')
        else:
            return render(request, 'home.html', {'error': 'invalid login'})
    else:
        return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        # to crete  user
        if request.POST['password'] == request.POST['Repeat_Password']:
            # both pass match
            # now check if a previous user exit
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'user is allready there'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                auth.login(request, user)

                return redirect(home)
        else:
            return render(request, 'signup.html', {'error': 'Passwords dont match'})
    else:
        return render(request, 'signup.html')


def logout(request):
    # auth.logout(home)
    auth.logout(request)
    request.session.flush()
    # request.user = AnonymousUser
    return render(request, 'home.html')


def servicepro(request):
    if request.method == "POST":
        servicename = request.POST.get('service_name')
        servicedate = request.POST.get('service_date')
        servicepro = Services(service_name=servicename, service_date=servicedate)
        servicepro.save()
    return render(request, 'servicepro.html')


def ClientView(request):
    if request.method == "POST":
        request_data = dict()
        request_data["first_name"] = request.POST.get('first_name')
        request_data["last_name"] = request.POST.get('last_name')
        request_data["email"] = request.POST.get('email')
        request_data["username"] = request.POST.get('username')
        #request_data["role"] = "client"
        password = request.POST.get('password')
        user = User.objects.create(**request_data)
        user.set_password(password)
        user.save()
    return render(request, 'admin_client.html')


def show1(request): 
    stud =Services.objects.all()
    print(stud)     
    return render(request,'show_appointmnt.html',{'stu': stud})

def show2 (request):
    st=User.objects.all()
    return render(request,'show_app.html',{'s': st})

def servicecreate(request):
    if request.method == "POST":
       request_data = dict()
       request_data["first_name"] = request.POST.get('first_name')
       request_data["last_name"] = request.POST.get('last_name')
       request_data["email"] = request.POST.get('email')
       request_data["username"] = request.POST.get('username')
       #request_data["role"] = "client"
       password = request.POST.get('password')
       user = User.objects.create(**request_data)
       user.set_password(password)
       user.save()
    return render(request, 'service_create.html')


def contacts(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number= request.POST.get('mobile_number')
        contacts = contact(first_name=first_name, last_name=last_name,email=email,mobile_number=mobile_number)
        contacts.save()
    return render(request, 'contact.html')



