from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from user.forms import SignupForm, ResetPasswordForm, LoginForm, ResetPasswordRequestForm
from user.models import UserDetails
from user.tokens import account_activation_token


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('netid') + '@nyu.edu'

            user = form.save(commit=False)
            user.is_active = False
            user.email = to_email
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your NYUnite Account!'
            message = render_to_string('activation_link_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "activation_link_sent.html")

    else:
        form = SignupForm()

    # if form.errors:
    #     Handle errors as popups
    return render(request, "signup.html", {'form': form})


def login_form(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            netid = form.cleaned_data.get('netid')
            password = form.cleaned_data.get('password')

            user = authenticate(request, netid = netid, password = password)
            if user is not None:
                login(request, user)
                return render(request, "dashboard.html")
            else:
                form.add_error("netid", "User not found")
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})


def logout(request):
    pass


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDetails.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'activate-signin.html')

    else:
        return render(request, 'activation_link_expired.html')


def password_reset_request(request):
    if request.method == 'POST':
        form = ResetPasswordRequestForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            netid = form.cleaned_data.get('netid')
            user = UserDetails.objects.get(netid=netid)
            to_email = netid + '@nyu.edu'
            current_site = get_current_site(request)
            mail_subject = 'Reset your NYUnite Account Password!'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "password_reset_check_email.html")
    else:
        form = ResetPasswordRequestForm()
    return render(request, 'password_reset_request_form.html', {'form': form})


def password_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDetails.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                error_bool, password = form.clean_password()
                if error_bool:
                    return render(request, 'password_reset_form.html', {'form': form})
                else:
                    user.set_password(password)
                    user.save()

                return render(request, 'password_reset_successful_signin.html')
        else:
            form = ResetPasswordForm()
        return render(request, 'password_reset_form.html', {'form': form})

    else:
        # HTML Page here to go back to the password reset request page
        return render(request, 'password_reset_request_form.html')


def dashboard(request):
    return render(request, "dashboard.html")
