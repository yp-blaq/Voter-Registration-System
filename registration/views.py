from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render,HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm
# we are importing modules for email confirmation in our views
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage



# Create your views here.

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request) #to get the current site domain

            #mail contents
            mail_subject = 'Confirm your email'
            message = render_to_string('reg_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            
            to_email = form.cleaned_data.get('email') #this gets the user email address from the form and sends the confirmation message
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')

            #login user after signup
            
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/registration/login")
    else:
        form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form} )

#we are creating an activate function to allow user login after successful confirmation
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        
        #return redirect("/registration/login")
        return HttpResponseRedirect('Thank you for your email confirmation. Now you can login your account.', "/registration/login")
    else:
        return HttpResponse('Activation link is invalid!')

#for login request
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/userpage")
            else:
                messages.error(request, "Invalid username or Password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/registration/login")