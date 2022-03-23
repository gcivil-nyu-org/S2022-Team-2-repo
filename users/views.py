from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import (
    UserRegisterForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    PreferencesPersonalityForm,
    PreferencesHobbiesForm,
    LoginForm,
)

from users.tokens import account_activation_token

User = get_user_model()


def home(request):
    return render(request, "users/home.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get("username") + "@nyu.edu"

            user = form.save(commit=False)
            user.is_active = False
            user.email = to_email
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your NYUnite Account!"
            message = render_to_string(
                "users/activation/activation_link_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "users/activation/activation_link_sent.html")

    else:
        form = UserRegisterForm()

    # TODO: if form.errors:
    #     Handle errors as popups
    return render(request, "users/authenticate/signup.html", {"form": form})


def login_form(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "dashboard.html")
            else:
                form.add_error("username", "User not found")
    else:
        form = LoginForm()
    return render(request, "users/authenticate/login.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    # TODO: if user is None:
    # User not found: Register again

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "users/activation/activate-signin.html")

    else:
        return render(request, "users/activation/activation_link_expired.html")


def password_reset_request(request):
    if request.method == "POST":
        form = ResetPasswordRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = User.objects.get(username=username)
            to_email = username + "@nyu.edu"
            current_site = get_current_site(request)
            mail_subject = "Reset your NYUnite Account Password!"
            message = render_to_string(
                "users/passwordreset/password_reset_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(
                request, "users/passwordreset/password_reset_check_email.html"
            )
    else:
        form = ResetPasswordRequestForm()
    return render(
        request, "users/passwordreset/password_reset_request_form.html", {"form": form}
    )


def password_reset(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                error_bool, password = form.clean_password()
                if error_bool:
                    return render(
                        request,
                        "users/passwordreset/password_reset_form.html",
                        {"form": form},
                    )
                else:
                    user.set_password(password)
                    user.save()

                return render(
                    request, "users/passwordreset/password_reset_successful_signin.html"
                )
        else:
            form = ResetPasswordForm()
        return render(
            request, "users/passwordreset/password_reset_form.html", {"form": form}
        )

    else:
        # TODO: HTML Page here to go back to the password reset request page
        return render(request, "users/passwordreset/password_reset_request_form.html")


def preferences_personality(request):
    context_dict = {"form": None}
    form = PreferencesPersonalityForm()

    if request.method == "GET":
        context_dict["form"] = form
    elif request.method == "POST":
        form = PreferencesPersonalityForm(request.POST)

        context_dict["form"] = form
        user = request.user
        if form.is_valid() and user is not None:
            prefs = form.save(commit=False)
            prefs.user = user
            prefs.save()
            print()
            return HttpResponseRedirect("/preferences/page2")

    return render(request, "users/preferences/preferences1.html", context_dict)


def preferences_hobbies(request):
    context_dict = {"form": None}
    form = PreferencesHobbiesForm()

    if request.method == "GET":
        context_dict["form"] = form
    elif request.method == "POST":
        form = PreferencesHobbiesForm(request.POST)
        context_dict["form"] = form
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data)
            return HttpResponseRedirect("/dashboard")

    return render(request, "users/preferences/preferences1.html", context_dict)


def dashboard(request):
    return render(request, "users/dashboard/dashboard.html")


def preferences(request):
    return render(request, "users/dashboard/dashboard_preferences.html")


# @login_required
# def users_list(request):
#     users = Profile.objects.exclude(user=request.user)
#     sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
#     sent_to = []
#     friends = []
#     for user in users:
#         friend = user.friends.all()
#         for f in friend:
#             if f in friends:
#                 friend = friend.exclude(user=f.user)
#         friends += friend
#     my_friends = request.user.profile.friends.all()
#     for i in my_friends:
#         if i in friends:
#             friends.remove(i)
#     if request.user.profile in friends:
#         friends.remove(request.user.profile)
#     random_list = random.sample(list(users), min(len(list(users)), 10))
#     for r in random_list:
#         if r in friends:
#             random_list.remove(r)
#     friends += random_list
#     for i in my_friends:
#         if i in friends:
#             friends.remove(i)
#     for se in sent_friend_requests:
#         sent_to.append(se.to_user)
#     context = {'users': friends, 'sent': sent_to}
#     return render(request, 'users/users_list.html', context)
#
#
# def friend_list(request):
#     p = request.user.profile
#     friends = p.friends.all()
#     context = {'friends': friends}
#     return render(request, 'users/friend_list.html', context)
#
#
# @login_required
# def send_friend_request(request, id):
#     user = get_object_or_404(User, id=id)
#     frequest, created = FriendRequest.objects.get_or_create(
#         from_user=request.user, to_user=user
#     )
#     return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
#
#
# @login_required
# def cancel_friend_request(request, id):
#     user = get_object_or_404(User, id=id)
#     frequest = FriendRequest.objects.filter(
#         from_user=request.user, to_user=user
#     ).first()
#     frequest.delete()
#     return HttpResponseRedirect('/users/{}'.format(user.profile.slug))
#
#
# @login_required
# def accept_friend_request(request, id):
#     from_user = get_object_or_404(User, id=id)
#     frequest = FriendRequest.objects.filter(
#         from_user=from_user, to_user=request.user
#     ).first()
#     user1 = frequest.to_user
#     user2 = from_user
#     user1.profile.friends.add(user2.profile)
#     user2.profile.friends.add(user1.profile)
#     if FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first():
#         request_rev = FriendRequest.objects.filter(
#             from_user=request.user, to_user=from_user
#         ).first()
#         request_rev.delete()
#     frequest.delete()
#     return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))
#
#
# @login_required
# def delete_friend_request(request, id):
#     from_user = get_object_or_404(User, id=id)
#     frequest = FriendRequest.objects.filter(
#         from_user=from_user, to_user=request.user
#     ).first()
#     frequest.delete()
#     return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))
#
#
# def delete_friend(request, id):
#     user_profile = request.user.profile
#     friend_profile = get_object_or_404(Profile, id=id)
#     user_profile.friends.remove(friend_profile)
#     friend_profile.friends.remove(user_profile)
#     return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))
#
#
# @login_required
# def profile_view(request, slug):
#     p = Profile.objects.filter(slug=slug).first()
#     u = p.user
#     sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
#     rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
#
#     friends = p.friends.all()
#
#     # is this user our friend
#     button_status = 'none'
#     if p not in request.user.profile.friends.all():
#         button_status = 'not_friend'
#
#         # if we have sent him a friend request
#         if (
#             len(
#                 FriendRequest.objects.filter(from_user=request.user).filter(
#                     to_user=p.user
#                 )
#             )
#             == 1
#         ):
#             button_status = 'friend_request_sent'
#
#         # if we have recieved a friend request
#         if (
#             len(
#                 FriendRequest.objects.filter(from_user=p.user).filter(
#                     to_user=request.user
#                 )
#             )
#             == 1
#         ):
#             button_status = 'friend_request_received'
#
#     context = {
#         'u': u,
#         'button_status': button_status,
#         'friends_list': friends,
#         'sent_friend_requests': sent_friend_requests,
#         'rec_friend_requests': rec_friend_requests,
#     }
#
#     return render(request, 'users/profile.html', context)
#
#
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(
#             request.POST, request.FILES, instance=request.user.profile
#         )
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('my_profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {
#         'u_form': u_form,
#         'p_form': p_form,
#     }
#     return render(request, 'users/edit_profile.html', context)
#
#
# @login_required
# def my_profile(request):
#     p = request.user.profile
#     you = p.user
#     sent_friend_requests = FriendRequest.objects.filter(from_user=you)
#     rec_friend_requests = FriendRequest.objects.filter(to_user=you)
#     friends = p.friends.all()
#
#     # is this user our friend
#     button_status = 'none'
#     if p not in request.user.profile.friends.all():
#         button_status = 'not_friend'
#
#         # if we have sent him a friend request
#         if (
#             len(
#                 FriendRequest.objects.filter(from_user=request.user).filter(to_user=you)
#             )
#             == 1
#         ):
#             button_status = 'friend_request_sent'
#
#         if (
#             len(
#                 FriendRequest.objects.filter(from_user=p.user).filter(
#                     to_user=request.user
#                 )
#             )
#             == 1
#         ):
#             button_status = 'friend_request_received'
#
#     context = {
#         'u': you,
#         'button_status': button_status,
#         'friends_list': friends,
#         'sent_friend_requests': sent_friend_requests,
#         'rec_friend_requests': rec_friend_requests,
#     }
#
#     return render(request, 'users/profile.html', context)
#
#
# @login_required
# def search_users(request):
#     query = request.GET.get('q')
#     object_list = User.objects.filter(username__icontains=query)
#     context = {'users': object_list}
#     return render(request, 'users/search_users.html', context)
