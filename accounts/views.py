from cgitb import html
from email.message import EmailMessage
from http.client import HTTPResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Account
from .forms import RegistrationForm

# email verification
from  django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_no = form.cleaned_data['phone_no']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
                )

            user.phone_no = phone_no
            user.save()

            # user activation start
            current_site = get_current_site(request)
            mail_subject = "Please active your account | GreatKart"
            message = render_to_string('accounts/account_varification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email =EmailMessage(mail_subject,message, to=[to_email]) 
            send_email.send()
            #  user activation start

            # messages.success(request,"")
            return redirect(f'/accounts/login/?command=verification&email={email}')
    else:
        form = RegistrationForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = auth.authenticate(email=email,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are logout")
    return redirect("login")

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated")
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password mail start
            current_site = get_current_site(request)
            mail_subject = "Reset your password | GreatKart"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email =EmailMessage(mail_subject,message, to=[to_email]) 
            send_email.send()
            # Reset Password mail ends
            messages.success(request,f"Password reset mail has send to your email [{email}]")
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist. If you want you can register here')
            return redirect('register')

    return render(request, 'accounts/forgotPassword.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,"Please Reset your Password")
        return redirect('resetPassword')
    else:
        messages.error(request,"This link has been expired")
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session['uid']
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Successful !")
            return redirect('login')

        else:
            messages.error(request, "Password Does not match")
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')