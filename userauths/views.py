from django.shortcuts import render,redirect
from userauths.form import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User


# User = settings.AUTH_USER_MODEL
# Create your views here.
def register_view(request):
    
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user =  form.save()
            username = form.cleaned_data.get("username")
            
            messages.success(request, f"Hey {username}, ban da dang ky thanh cong")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("core:index")
        print("dang ky thanh cong")
    
    else:
        print("khong the dang ky")
    
    form = UserRegisterForm()
    
    context = {
        'form' : form,
    }
    return render(request, "userauths/sign-up.html",context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"ban da dang nhap")
        return redirect("core:index")
    
    
    
    if request.method == "POST":
        email = request.POST.get("email")
        password =  request.POST.get("password")
        
        # try:
        #     user = User.object.get(email = email)
            
            
        # except:
        #     messages.warning(request,f"User with {email} does not exit")
            
        user  =  authenticate(request, email = email, password = password)
           
        if user is not None:
            login(request,user)
            messages.success(request,"dang nhap thanh cong")
            return redirect("core:index")
        else:
             messages.warning(request,"nguoi dun gko ton tai")
        
    return render(request, "userauths\sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request,"you logged out")
    return redirect("userauths:sign-in")