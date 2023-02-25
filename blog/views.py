from django.shortcuts import redirect, render
from .forms import SignUpForm, EditUser
from .models import Post
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash

# Create your views here.
def home(request):
    posts=Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})


def about(request):
    if request.user.is_authenticated:
        return render(request, 'blog/about.html')
    else:
        return redirect ('login')


def contact(request):
    if request.user.is_authenticated:
        return render(request, 'blog/contact.html')
    else:
        return redirect ('login')



def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = SignUpForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'User Created!!')
        else:
            fm = SignUpForm()
        return render (request, 'blog/signup.html', {'form':fm})
    else:
        return redirect ('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                un = fm.cleaned_data['username']
                pw = fm.cleaned_data['password']
                user = authenticate(username=un, password=pw)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            fm = AuthenticationForm()
        return render(request, 'blog/login.html', {'form':fm})
    else:
        return redirect ('/')

def user_logout(request):
    logout(request)
    return redirect('/')

def changepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data = request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'Password Has Changed Successfully')
                update_session_auth_hash(request, fm.user)
                return redirect ('/')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'blog/changepass.html', {'form':fm})
    else:
        return redirect ('login')

def profile_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = EditUser(request.POST, instance=request.user)
            if fm.is_valid():
                fm.save()
                messages.success(request, 'User Profile Updated')
        else:
            fm = EditUser(instance=request.user)
        return render(request, 'blog/profile.html', {'name':request.user.first_name, 'form':fm})
    else:
        return redirect ('login')