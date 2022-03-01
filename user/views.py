from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage

from user.forms import SignupForm
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
            print(to_email)
            email.send()

            HttpResponse('Please check your NYU Inbox.')
            return render(request, "home.html")

    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})


def login(request):
    return render(request, "login.html")


def logout(request):
    pass


def activate(request):
    return HttpResponse('Thank you very much!')
