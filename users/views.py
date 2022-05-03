import os
from collections import defaultdict
from datetime import datetime, time, date, timedelta
from typing import List

import numpy as np
import requests
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
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import ListView, DetailView

from django_private_chat2.models import MessageModel
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
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))

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


def reactivate(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))

    if request.method == "POST":
        try:
            username = request.POST.get("username")
            user = User.objects.get(username=username)
            if not user.is_active:
                to_email = username + "@nyu.edu"
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
        except Exception as e:
            return render(request, "reactivate.html", {"err": e})


def login_form(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))

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
            try:
                user = User.objects.get(username=username)
            except Exception:
                form = ResetPasswordRequestForm()
                form.errors["username"] = "User with that NetID does not exist."
                return render(
                    request,
                    "users/passwordreset/password_reset_request_form.html",
                    {"form": form},
                )

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
                password = form.cleaned_data.get("new_password1")
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
    except Exception:  # pragma: no cover
        prof = Profile(user=request.user)
        prof.save()

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=prof)
        if form.is_valid():
            ans = form.save()

            if "image" in request.FILES:  # pragma: no cover
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
    except Exception:  # pragma: no cover
        prof = Profile(user=request.user)
        prof.save()

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=prof)
        if form.is_valid():
            ans = form.save()

            if "image" in request.FILES:  # pragma: no cover
                ans.image = request.FILES["image"]

            ans.save()
            return HttpResponseRedirect("/dashboard")
    else:
        form = ProfileUpdateForm(instance=prof)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required()
def delete_profile(request):
    try:
        u = User.objects.get(username=request.user.username)
        u.delete()
        logout(request)
        return HttpResponseRedirect(reverse("home"))
    except Exception as e:
        return render(request, "dashboard_preferences.html", {"err": e})


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


def recent_contacts(request):
    messages = (
        MessageModel.objects.all()
        .filter(Q(sender_id=request.user.id) | Q(recipient_id=request.user.id))
        .order_by("-modified")
    )

    contacts = []
    for message in messages:
        if message.recipient_id != request.user.id:
            contact = message.recipient_id
        else:
            contact = message.sender_id
        if contact not in contacts and len(contacts) < 5:
            contacts.append(contact)

    recent = []
    for contact in contacts:
        recent.append(User.objects.get(pk=contact))

    return recent


@login_required()
def favorite(request):
    user1 = User.objects.get(pk=request.user.id).profile

    user2_id = request.POST.get("favorite")
    user2 = User.objects.get(pk=user2_id).profile
    if user2 in user1.favorites.all():
        user1.favorites.remove(user2)
    else:
        user1.favorites.add(user2)
    return HttpResponse()


@login_required
def dashboard(request):
    recent = recent_contacts(request)
    favorites = request.user.profile.favorites.all()
    context = {"recent": recent, "favorites": favorites}
    return render(request, "users/dashboard/dashboard.html", context)


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
        .exclude(id__in=request.user.profile.blocked.all().values_list("id", flat=True))
        .exclude(
            id__in=request.user.profile.blockers.all().values_list("id", flat=True)
        )
        .exclude(is_staff="t")
    )
    return search_query, query_set


@login_required
def search(request):
    search_query, query_set = get_search(request)
    friend_list = request.user.profile.friends.all()
    friend_list_ids = []
    for friend in friend_list:  # pragma: no cover
        friend_list_ids.append(friend.id)

    return render(
        request,
        "users/search/search.html",
        {"queryset": query_set, "query": search_query, "friend_list": friend_list_ids},
    )


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
    request_rev = FriendRequest.objects.filter(
        from_user=user, to_user=from_user
    ).first()
    if request_rev:
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
    if frequest:
        frequest.delete()


@login_required
def decline_request_query(request):
    user_id = request.POST.get("declineRequest")
    if user_id is not None:
        decline_request(request.user, user_id)
    return HttpResponse()


@login_required()
def remove_friend(request):
    user1 = User.objects.get(pk=request.user.id).profile
    user2_id = request.POST.get("remove")
    user2 = User.objects.get(pk=user2_id).profile

    if user1.profile in user2.profile.favorites.all():
        user2.profile.favorites.remove(user1.profile)
    if user2.profile in user1.profile.favorites.all():
        user1.profile.favorites.remove(user2.profile)

    user1.friends.remove(user2)
    user2.friends.remove(user1)

    return HttpResponse()


@login_required
def block(request):
    blocker = User.objects.get(id=request.user.id)
    blocked = User.objects.get(id=request.POST.get("blocked"))

    if blocked.profile in blocker.profile.friends.all():
        blocker.profile.friends.remove(blocked.profile)
        blocked.profile.friends.remove(blocker.profile)
    if blocked.profile in blocker.profile.favorites.all():
        blocker.profile.favorites.remove(blocked.profile)
    if blocker.profile in blocked.profile.favorites.all():
        blocked.profile.favorites.remove(blocker.profile)

    blocker.profile.blocked.add(blocked.profile)
    blocked.profile.blockers.add(blocker.profile)

    return HttpResponse()


@login_required()
def blocked_list(request):
    user = User.objects.get(id=request.user.id)
    blocked = user.profile.blocked.all()
    return render(request, "users/dashboard/blocked.html", {"blocked": blocked})


@login_required()
def unblock(request):
    blocker = User.objects.get(id=request.user.id)
    blocked = User.objects.get(id=request.POST.get("unblock"))

    if blocked.profile in blocker.profile.blocked.all():
        blocker.profile.blocked.remove(blocked.profile)
    if blocker.profile in blocked.profile.blockers.all():
        blocked.profile.blockers.remove(blocker.profile)

    return HttpResponse()


@login_required
def my_friends(request):
    invitations = FriendRequest.objects.filter(to_user_id=request.user)
    p = request.user.profile
    friends = p.friends.all()
    favorites = p.favorites.all()
    context = {"friends": friends, "invitations": invitations, "favorites": favorites}
    return render(request, "users/friends/my_friends.html", context)


@login_required
def notifications(request):
    num_notifications = len(FriendRequest.objects.filter(to_user_id=request.user))
    return HttpResponse(str(num_notifications), content_type="text/plain")


@login_required
def chat_notifications(request):
    num_notifications = len(
        MessageModel.objects.all()
        .filter(recipient_id=request.user.id)
        .filter(read=False)
    )
    return HttpResponse(str(num_notifications), content_type="text/plain")


@login_required()
def reject_suggestion(request):
    user_id = request.POST.get("friendID")
    if user_id is not None:
        # Add them to request.user profile seen user
        rejector = User.objects.get(id=request.user.id)
        rejectee = User.objects.get(id=user_id)
        rejector.profile.seen_users.add(rejectee.profile)

    return HttpResponse()


@login_required()
def approve_suggestion(request):
    user_id = request.POST.get("friendID")
    if user_id is not None:
        # Add them to request.user profile seen user
        accepter = User.objects.get(id=request.user.id)
        acceptee = User.objects.get(id=user_id)
        accepter.profile.seen_users.add(acceptee.profile)

        # Send a friend request
        send_friend_request(request.user, user_id)

    return HttpResponse()


def get_null_preferences():
    personality_query = Q(personality_type__exact="")
    movie_query = Q(movie_choices__exact="")
    food_query = Q(food_choices__exact="")
    null_objects = Preference.objects.filter(
        personality_query | movie_query | food_query
    )
    return null_objects


def get_matches(user):
    matches = list(
        User.objects.exclude(id=user.id)
        .exclude(id__in=user.profile.friends.all().values_list("id", flat=True))
        .exclude(id__in=user.profile.seen_users.all().values_list("id", flat=True))
        .exclude(id__in=user.profile.blocked.all().values_list("id", flat=True))
        .exclude(id__in=user.profile.blockers.all().values_list("id", flat=True))
        .exclude(is_staff="t")
    )
    preference_fields = Preference._meta.get_fields()
    null_preferences = get_null_preferences()

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

    similarity = []
    common_interests = []
    good_matches = []

    for match in matches:
        count = 0

        try:
            prefs = Preference.objects.get(user=match)
            if prefs in null_preferences:
                matches.remove(match)
                continue
        except Exception:
            matches.remove(match)
            continue

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

        # Whatever threshold we decide
        if count >= 3:
            similarity.append(count)
            common_interests.append(list(common_list))
            good_matches.append(match)

    # Reorder the matches by similarity
    similarity = np.array(similarity)
    good_matches = np.array(good_matches)
    common_interests = np.array(common_interests)
    inds = similarity.argsort()[::-1]
    ordered_matches = good_matches[inds]
    ordered_interests = common_interests[inds]

    return ordered_matches, ordered_interests


@login_required
def friend_finder(request):
    null_objects = get_null_preferences()

    try:
        prefs = Preference.objects.get(user=request.user)
        if prefs in null_objects:
            return HttpResponseRedirect("/preferences/page1")
    except Exception:
        return HttpResponseRedirect("/preferences/page1")

    matches, interests = get_matches(request.user)
    match_list = []

    for index, match in enumerate(matches):
        matched_hobbies = interests[index]
        similar_choices = defaultdict(list)

        for i in matched_hobbies:
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


@login_required()
def activity_search(request):
    MY_API_KEY = os.environ.get("YELP_API_KEY")
    headers = {"Authorization": "Bearer {}".format(MY_API_KEY)}
    search_api_url = "https://api.yelp.com/v3/events"

    params = {
        "location": "New York, NY",
        "start_date": int(datetime.now().timestamp()),
        "limit": 12,
        "offset": 0,
    }

    category = request.GET.get("category", None)
    if category is not None and category != "all":
        params["categories"] = category

    selected_time = request.GET.get("time", None)
    idx = date.today().weekday() + 2

    if selected_time == "today":
        params["end_date"] = int(datetime.combine(datetime.now(), time.max).timestamp())

    elif selected_time == "tomorrow":
        params["start_date"] = int(
            datetime.combine(date.today() + timedelta(days=1), time.min).timestamp()
        )
        params["end_date"] = int(
            datetime.combine(date.today() + timedelta(days=1), time.max).timestamp()
        )

    elif selected_time == "weekend":
        params["end_date"] = int(
            datetime.combine(date.today() + timedelta(7 - idx), time.min).timestamp()
        )
        params["end_date"] = int(
            datetime.combine(
                date.today() + timedelta(7 - idx + 1), time.max
            ).timestamp()
        )

    # Assuming week ends on Saturday night
    elif selected_time == "this-week":
        params["end_date"] = int(
            datetime.combine(date.today() + timedelta(7 - idx), time.max).timestamp()
        )

    elif selected_time == "next-week":
        params["start_date"] = int(
            datetime.combine(
                date.today() + timedelta(7 - idx + 1), time.min
            ).timestamp()
        )
        params["end_date"] = int(
            datetime.combine(date.today() + timedelta(14 - idx), time.min).timestamp()
        )

    selected_free = request.GET.get("free", None)
    if selected_free == "free":
        params["is_free"] = True

    response = requests.get(search_api_url, headers=headers, params=params, timeout=5)
    data = response.json()

    return JsonResponse(data["events"], safe=False)


@login_required()
def activity(request):
    # event_data = activity_search(request)
    return render(request, "users/activity.html")
