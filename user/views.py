from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_str

from user.forms import SignupForm, ResetPasswordForm
from user.models import UserDetails
from user.tokens import account_activation_token


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your NYUnite Account!'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            to_email = form.cleaned_data.get('netID') + '@nyu.edu'
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "activation_link_email.html")

    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})


def login(request):
    return render(request, "login.html")


def logout(request):
    pass


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDetails.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        return HttpResponse("Thanks for activating your account!")

    else:
        return HttpResponse("Activation link is not valid!")


def password_reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # current_site = get_current_site(request)
            mail_subject = 'Reset your NYUnite Password!'
            message = 'Reset your password!'

            to_email = form.cleaned_data.get('netID')+ '@nyu.edu'
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

        return render(request, 'password_reset_check_email.html')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})
