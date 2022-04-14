from typing import List

from collections import defaultdict

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView
import numpy as np

from users.forms import (
    ProfileUpdateForm,
    UserRegisterForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    PreferencesPersonalityForm,
    LoginForm,
    PreferencesHobbiesForm,
    PreferencesExploreForm,
)
from users.models import Preference, Profile, FriendRequest
from users.preferences import interests_choices

from users.tokens import account_activation_token

User = get_user_model()


def home(request):
    return render(request, "users/home.html")


def signup(request):  # pragma: no cover
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
                try:
                    Profile.objects.get(user=request.user)
                except Exception:
                    return redirect("/profile/setup")

                next_url = request.GET.get("next", "/dashboard")
                return HttpResponseRedirect(next_url)
            else:
                form.add_error("username", "User with that credentials not found.")
    else:
        form = LoginForm()
    return render(request, "users/authenticate/login.html", {"form": form})


@login_required()
def logout_request(request):
    user = request.user
    if user is not None and user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("/")


def activate(request, uidb64, token):  # pragma: no cover
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
        login(request, user)
        return profile_setup(request)

    else:
        return render(request, "users/activation/activation_link_expired.html")


def password_reset_request(request):  # pragma: no cover
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


def password_reset(request, uidb64, token):  # pragma: no cover
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = ResetPasswordForm(request.POST)
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


@login_required()
def profile_setup(request):
    prof = None

    try:
        prof = Profile.objects.get(user=request.user)
    except Exception:
        prof = Profile(user=request.user)
        prof.save()

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=prof)
        if form.is_valid():
            ans = form.save()

            if "image" in request.FILES:
                ans.image = request.FILES["image"]

            ans.save()
            return HttpResponseRedirect("/preferences/page1")
    else:
        form = ProfileUpdateForm(instance=prof)
    return render(request, "users/preferences/profile_setup.html", {"form": form})


@login_required()
def update_profile(request):
    prof = None

    try:
        prof = Profile.objects.get(user=request.user)
    except Exception:
        prof = Profile(user=request.user)
        prof.save()

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=prof)
        if form.is_valid():
            ans = form.save()

            if "image" in request.FILES:
                ans.image = request.FILES["image"]

            ans.save()
            return HttpResponseRedirect("/dashboard")
    else:
        form = ProfileUpdateForm(instance=prof)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required()
def preferences_personality(request):
    prefs = None

    try:
        prefs = Preference.objects.get(user=request.user)
    except Exception:
        prefs = Preference(user=request.user)
        prefs.save()

    if request.method == "POST":
        form = PreferencesPersonalityForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/preferences/page2")
    else:
        form = PreferencesPersonalityForm(instance=prefs)
    return render(request, "users/preferences/preferences1.html", {"form": form})


@login_required
def preferences_hobbies(request):
    try:
        prefs = Preference.objects.get(user=request.user)
    except Exception:
        prefs = Preference(user=request.user)
        prefs.save()

    if request.method == "POST":
        form = PreferencesHobbiesForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/preferences/page3")
    else:
        form = PreferencesHobbiesForm(instance=prefs)
    return render(request, "users/preferences/preferences2.html", {"form": form})


@login_required
def preferences_explore(request):
    try:
        prefs = Preference.objects.get(user=request.user)
    except Exception:
        prefs = Preference(user=request.user)
        prefs.save()

    if request.method == "POST":
        form = PreferencesExploreForm(request.POST, instance=prefs)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/dashboard")
    else:
        form = PreferencesExploreForm(instance=prefs)
    return render(request, "users/preferences/preferences3.html", {"form": form})


class FriendsListView(LoginRequiredMixin, ListView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        return profile.friends.all()

    def render_to_response(self, context, **response_kwargs):
        profiles: List[User] = context["object_list"]

        data = [
            {
                "username": profile.user.get_username(),
                "pk": str(profile.user.pk),
                "first_name": str(profile.user.first_name),
                "last_name": str(profile.user.last_name),
                "image": profile.image.url,
            }
            for profile in profiles
        ]
        return JsonResponse(data, safe=False, **response_kwargs)


class SelfView(LoginRequiredMixin, DetailView):
    http_method_names = [
        "get",
    ]

    model = Profile

    def render_to_response(self, context, **response_kwargs):
        profile: Profile = context["object"]

        data = {
            "username": profile.user.get_username(),
            "pk": str(profile.user.pk),
            "first_name": str(profile.user.first_name),
            "last_name": str(profile.user.last_name),
            "image": profile.image.url,
        }
        return JsonResponse(data, safe=False, **response_kwargs)


@login_required
def self_info(request):
    profile = Profile.objects.get(user=request.user)

    data = {
        "username": profile.user.get_username(),
        "pk": str(profile.user.pk),
        "first_name": str(profile.user.first_name),
        "last_name": str(profile.user.last_name),
        "image": profile.image.url,
    }
    return JsonResponse(data, safe=False)


@login_required
def dashboard(request):
    return render(request, "users/dashboard/dashboard.html")


@login_required
def preferences(request):
    try:
        prefs = Preference.objects.get(user=request.user)
    except Exception:
        prefs = Preference(user=request.user)
        prefs.save()

    return render(
        request,
        "users/dashboard/dashboard_preferences.html",
        {"user": request.user, "prefs": model_to_dict(prefs)},
    )


# Helper function for searching
def get_search(request):
    search_query = request.GET.get("navSearch", "").strip()
    print(search_query)
    username_query = Q(username__icontains=search_query)
    fullname_query = Q(full_name__icontains=search_query)

    query_set = (
        User.objects.annotate(full_name=Concat("first_name", V(" "), "last_name"))
        .filter(username_query | fullname_query)
        .exclude(id=request.user.id)
        .exclude(is_staff="t")
    )
    return search_query, query_set


# Helper function
def send_friend_request(user, id):
    to_user = User.objects.get(id=id)
    FriendRequest.objects.get_or_create(from_user=user, to_user=to_user)


@login_required
def friend_request_query(request):
    user_id = request.POST.get("friendRequest")
    if user_id is not None:
        send_friend_request(request.user, user_id)
    return HttpResponse()


def accept_request(user, id):
    from_user = User.objects.get(id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if FriendRequest.objects.filter(from_user=user, to_user=from_user).first():
        request_rev = FriendRequest.objects.filter(
            from_user=user, to_user=from_user
        ).first()
        request_rev.delete()
    frequest.delete()


@login_required
def accept_request_query(request):
    user_id = request.POST.get("acceptRequest")
    if user_id is not None:
        accept_request(request.user, user_id)
    return HttpResponse()


def decline_request(user, id):
    from_user = User.objects.get(id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=user).first()
    frequest.delete()


@login_required
def decline_request_query(request):
    user_id = request.POST.get("declineRequest")
    if user_id is not None:
        decline_request(request.user, user_id)
    return HttpResponse()


@login_required
def search(request):
    search_query, query_set = get_search(request)
    friend_list = request.user.profile.friends.all()
    friend_list_ids = []
    for friend in friend_list:
        friend_list_ids.append(friend.id)

    return render(
        request,
        "users/search/search.html",
        {"queryset": query_set, "query": search_query, "friend_list": friend_list_ids},
    )


@login_required
def my_friends(request):
    invitations = FriendRequest.objects.filter(to_user_id=request.user)
    p = request.user.profile
    friends = p.friends.all()
    context = {"friends": friends, "invitations": invitations}
    return render(request, "users/friends/my_friends.html", context)


@login_required
def notifications(request):
    num_notifications = len(FriendRequest.objects.filter(to_user_id=request.user))
    return HttpResponse(str(num_notifications), content_type="text/plain")


def reject_suggestion(request):
    user_id = request.POST.get("friendID")
    if user_id is not None:
        # Add them to request.user profile seen user
        rejector = User.objects.get(id=request.user.id)
        rejectee = User.objects.get(id=user_id)
        rejector.profile.seen_users.add(rejectee.profile)

    return HttpResponse()


def approve_suggestion(request):
    user_id = request.POST.get("friendID")
    if user_id is not None:
        # Add them to request.user profile seen user
        accepter = User.objects.get(id=request.user.id)
        acceptee = User.objects.get(id=user_id)
        accepter.profile.seen_users.add(acceptee.profile)
        print(accepter.profile.seen_users)

        # Send a friend request
        send_friend_request(request.user, user_id)

    return HttpResponse()


def get_matches(user):
    matches = list(
        User.objects.exclude(id=user.id)
        .exclude(id__in=user.profile.friends.all().values_list("id", flat=True))
        .exclude(id__in=user.profile.seen_users.all().values_list("id", flat=True))
        .exclude(is_staff="t")
    )
    preference_fields = Preference._meta.get_fields()

    similarity = []
    common_interests = []
    not_interested = [
        "Movie_NI",
        "MUSIC_NI",
        "Cookeat_NI",
        "Travel_NI",
        "Art_NI",
        "Dance_NI",
        "Sports_NI",
        "Pet_NI",
        "Nyc_NI",
    ]

    for match in matches:
        count = 0

        common_list = set()

        for i in range(4, len(preference_fields)):
            val1 = preference_fields[i].value_from_object(match.preference)
            val2 = preference_fields[i].value_from_object(user.preference)
            common = set(val1).intersection(list(val2))
            common_list = common_list.union(common)
            count += len(common)

        for ele in not_interested:
            if ele in common_list:
                common_list.remove(ele)

        similarity.append(count)
        common_interests.append(list(common_list))

    # Reorder the matches by similarity
    similarity = np.array(similarity)
    matches = np.array(matches)
    common_interests = np.array(common_interests)
    inds = similarity.argsort()[::-1]
    ordered_matches = matches[inds]
    ordered_interests = common_interests[inds]

    return ordered_matches, ordered_interests


@login_required
def friend_finder(request):
    matches, interests = get_matches(request.user)
    match_list = []
    similar_choices = defaultdict(list)
    print(matches)
    for index, match in enumerate(matches):
        print(type(interests[index]))
        matched_hobbies = interests[index]
        print(interests[index])
        print(type(match))
        print(match)
        print(matched_hobbies)
        for i in matched_hobbies:
            print(interests_choices[i])
            if i.startswith("Movie"):
                similar_choices["Movie Choices"].append(interests_choices[i])
            elif i.startswith("MUSIC"):
                similar_choices["Music Choices"].append(interests_choices[i])
            elif i.startswith("Cookeat"):
                similar_choices["Food Choices"].append(interests_choices[i])
            elif i.startswith("Travel"):
                similar_choices["Travel Choices"].append(interests_choices[i])
            elif i.startswith("Art"):
                similar_choices["Art Choices"].append(interests_choices[i])
            elif i.startswith("Dance"):
                similar_choices["Dance Choices"].append(interests_choices[i])
            elif i.startswith("Sports"):
                similar_choices["Sports Choices"].append(interests_choices[i])
            elif i.startswith("Pet"):
                similar_choices["Pets Choices"].append(interests_choices[i])
            elif i.startswith("Nyc"):
                similar_choices["NYC Choices"].append(interests_choices[i])
            elif i.startswith("Staygo") or i.startswith("Personality"):
                similar_choices["Personality Type"].append(interests_choices[i])
        print(similar_choices)
        match_list.append(
            {
                "id": match.id,
                "username": match.username,
                "first_name": match.first_name,
                "last_name": match.last_name,
                "profile": Profile.objects.get(user=match),
                "common_interests": dict(similar_choices),
            }
        )
    return render(request, "users/friends/friend_finder.html", {"matches": match_list})


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
#     return render(request, 'users/edit_profile.html', context)
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
#     return render(request, 'users/edit_profile.html', context)
#
#
# @login_required
# def search_users(request):
#     query = request.GET.get('q')
#     object_list = User.objects.filter(username__icontains=query)
#     context = {'users': object_list}
#     return render(request, 'users/search_users.html', context)
