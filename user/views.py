from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from user.forms import SignupForm, ResetPasswordForm, LoginForm
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
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "activation_link_email.html")

    else:
        form = SignupForm()

    # if form.errors:
    #     Handle errors as popups
    return render(request, "signup.html", {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Database stuff here later...
            # Check if the user is active
            return render(request, "dashboard.html")
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
        # Set user to active
        return render(request, 'activate-signin.html')

    else:
        return HttpResponse("Activation link is not valid!")


def password_reset_request(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            netid = form.cleaned_data.get('netid')
            print(netid)
            user = UserDetails.objects.get(netid=netid)
            print(user)
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
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


def password_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDetails.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Set user to active
        return render(request, 'activate-signin.html')

    else:
        return HttpResponse("Activation link is not valid!")


def dashboard(request):
    return render(request, "dashboard.html")
